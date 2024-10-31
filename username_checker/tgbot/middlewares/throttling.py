from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from username_checker.tgbot.throttling.exc import CancelHandlerError, ThrottledError
from username_checker.tgbot.utils.data import MiddlewareData

MAX_EXCEEDED_COUNT = 2


class ThrottlingMiddleware(BaseMiddleware):

    """A middleware class that implements rate limiting for incoming messages."""

    def __init__(self, limit: float = 0.5):
        self.rate_limit = limit

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[Message, MiddlewareData], Awaitable[Any]],
        event: Message,
        data: MiddlewareData,
    ) -> Any:
        """Calls the throttling middleware, applying rate limiting to incoming messages."""
        try:
            await self.on_process_event(event, data)
        except CancelHandlerError:
            # Cancel current handler
            return None

        return await handler(event, data)

    async def on_process_event(self, event: Message, data: MiddlewareData) -> Any:
        """
        Process an incoming event, applying rate limiting using the ThrottleManager.

        :param event: The incoming event to be processed.
        :type event: Message

        :param data: Additional data associated with the event.
        :type data: MiddlewareData

        :return: The result of the event processing, or None if the handler is cancelled.
        :rtype: Any
        """
        throttle_manager = data["throttle_manager"]
        try:
            await throttle_manager.throttle(self.rate_limit, user_id=data["event_from_user"].id, chat_id=data["event_chat"].id)
        except ThrottledError as err:
            await self.event_throttled(event, err, data)
            raise CancelHandlerError from None

    async def event_throttled(self, event: Message, throttled: ThrottledError, data: MiddlewareData) -> None:
        """
        Asynchronously handles the event when a user sends too many messages within a certain time frame.

        :param event: The incoming message event.
        :type event: Message

        :param throttled: The throttling error object.
        :type throttled: ThrottledError

        :return: None
        :rtype: None
        """
        # Calculate how many time is left till the block ends
        i18n = data["i18n"]
        logger = data["logger"]
        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count <= MAX_EXCEEDED_COUNT:
            await logger.ainfo("Throttled: user_id=%s, chat_id=%s, delta=%s", data["event_from_user"].id, data["event_chat"].id, delta)
            await event.answer(i18n.get("throttling-try-again-text-user", seconds=f"{delta:.2f}"))
