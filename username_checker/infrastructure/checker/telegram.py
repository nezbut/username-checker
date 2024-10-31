import asyncio
from types import TracebackType
from typing import Any, Optional

from aiohttp import ClientSession
from aiohttp.hdrs import USER_AGENT
from structlog.stdlib import BoundLogger

from username_checker.core.entities.username import Username, UsernameStatus
from username_checker.core.interfaces.username import UsernameChecker


class TelegramUsernameChecker(UsernameChecker):

    """A class for checking the username status in Telegram."""

    def __init__(self, logger: BoundLogger, session: Optional[ClientSession] = None) -> None:
        self._session_or_none = session
        self._base_url = "https://fragment.com"
        self._logger = logger
        self._session: ClientSession

    async def check(self, username: Username) -> UsernameStatus:
        """
        Checking a username status in Telegram.

        :param username: The username to be checked.
        :type username: Username
        :return: username status
        :rtype: UsernameStatus
        """
        try:
            json_data = await self._fragment_request(username.value)
        except ValueError:
            await self._logger.adebug("Return status: %s", UsernameStatus.UNKNOWN)
            return UsernameStatus.UNKNOWN

        if "h" not in json_data:
            await self._logger.adebug("Return status: %s", UsernameStatus.AVAILABLE)
            return UsernameStatus.AVAILABLE
        await self._logger.adebug("Return status: %s", UsernameStatus.NOT_AVAILABLE)
        return UsernameStatus.NOT_AVAILABLE

    async def close(self) -> None:
        """Closes the client."""
        await self._session.close()
        await asyncio.sleep(0.25)

    async def __aenter__(self) -> "TelegramUsernameChecker":
        """Asynchronous context manager entry point."""
        log_msg = "Startup Telegram Username Checker with default session" \
            if self._session_or_none is None else "Startup Telegram Username Checker with custom session"
        self._session = self._session_or_none or ClientSession(
            base_url=self._base_url,
            headers={
                USER_AGENT: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
            },
        )
        await self._logger.ainfo(log_msg)
        return self

    async def _fragment_request(self, username: str) -> Any:
        headers = self._headers(username)
        url = f"/username/{username}"
        async with self._session.get(url, headers=headers) as response:
            await self._logger.ainfo("New response status: %s to %s. Reason: %s", response.status, f"{self._base_url}{url}", response.reason)
            return await response.text()

    async def __aexit__(self, exc_type: Optional[type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        """Asynchronous context manager exit point."""
        await self.close()
        await self._logger.ainfo("Close Telegram Username Checker")

    def _headers(self, username: str) -> dict[str, Any]:
        return {
            "X-Aj-Referer": f"{self._base_url}/?query={username}",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
        }
