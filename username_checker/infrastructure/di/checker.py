from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide

from username_checker.common.log.configuration import LoggerName
from username_checker.common.log.installer import LoggersInstaller
from username_checker.core.interfaces.username import UsernameChecker
from username_checker.infrastructure.checker.telegram import TelegramUsernameChecker


class UsernameCheckerProvider(Provider):

    """Provider for username checkers."""

    @provide(scope=Scope.APP)
    async def get_tg_username_checker(self, installer: LoggersInstaller) -> AsyncIterable[UsernameChecker]:
        """Returns a tg username checker."""
        logger = installer.get_logger(LoggerName.USERNAME_CHECKER)
        async with TelegramUsernameChecker(logger) as checker:
            yield checker


def get_username_checkers_providers() -> list[Provider]:
    """Returns a list of username checkers providers for di."""
    return [
        UsernameCheckerProvider(),
    ]
