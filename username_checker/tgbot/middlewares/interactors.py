from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from username_checker.tgbot.utils.data import MiddlewareData


class InteractorsMiddleware(BaseMiddleware):

    """Middleware for interactors."""

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """Interactors Middleware"""
        return await handler(event, data)
