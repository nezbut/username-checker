from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluentogram import TranslatorHub

from username_checker.tgbot.utils.data import MiddlewareData


class I18NMiddleware(BaseMiddleware):

    """I18N middleware."""

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """I18N middleware."""
        user = data["current_user"].user
        container = data["dishka_container"]
        hub: TranslatorHub = await container.get(TranslatorHub)
        translator = hub.get_translator_by_locale(locale=user.language.value)
        data["i18n"] = translator
        data["i18n_getter"] = translator.get

        return await handler(event, data)
