from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Any, Optional, Union

from adaptix import dump, load
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from username_checker.core.entities.user import LanguageLocale, User
from username_checker.core.services import user as user_service
from username_checker.infrastructure.clients.cache.key import UserCacheKey
from username_checker.infrastructure.proxy.user import CurrentUserProxy
from username_checker.tgbot.utils.data import MiddlewareData


class TrackUserMiddleware(BaseMiddleware):

    """Track user middleware."""

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """Track user middleware."""
        cache = data["cache"]
        holder = data["holder_dao"]
        user_aiogram = data["event_from_user"]
        logger = data["logger"]
        user_cache_key = UserCacheKey(user_aiogram.id)
        user_data = (user_aiogram.id,
                     user_aiogram.username or user_aiogram.first_name)
        await logger.adebug("Start track for user. id=%s, username=%s", *user_data)
        user_from_cache: Optional[dict[str, Any]] = await cache.get(user_cache_key)

        if not user_from_cache:
            await logger.adebug("User is not in cache. id=%s, username=%s", *user_data)
            user_from_db = await user_service.get_by_id(user_aiogram.id, holder.user)
            if not user_from_db:
                await logger.adebug("User is not in database. id=%s, username=%s", *user_data)
                user_from_db = User(
                    id=user_aiogram.id,
                    username=user_aiogram.username or user_aiogram.first_name,
                    joined_us=datetime.now(UTC),
                    last_activity=datetime.now(UTC),
                    language=LanguageLocale(
                        user_aiogram.language_code or "en",
                    ),
                    is_admin=False,
                    is_superuser=False,
                    is_banned=False,
                )
            else:
                await logger.adebug("Update user. id=%s, username=%s", *user_data)
                user_from_db.username = user_aiogram.username or user_aiogram.first_name
                user_from_db.last_activity = datetime.now(UTC)
            await user_service.upsert_user(user_from_db, holder.user)
            await holder.commit()
            await logger.adebug("Upsert user in database. id=%s, username=%s", *user_data)
            await cache.set(user_cache_key, dump(user_from_db))
            await logger.adebug("Set user in cache. id=%s, username=%s", *user_data)
            current_user = user_from_db
        else:
            await logger.adebug("User is in cache. id=%s, username=%s", *user_data)
            current_user = load(user_from_cache, User)

        data["current_user"] = CurrentUserProxy(
            user=current_user,
            user_proxy=data["user_proxy"],
        )
        return await handler(event, data)


class BannedUserMiddleware(BaseMiddleware):

    """Banned user middleware."""

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: MiddlewareData,
    ) -> Any:
        """Banned user middleware."""
        current_user = data["current_user"]
        i18n = data["i18n"]

        if current_user.user.is_banned:
            return event.answer(i18n.get("user-banned-text"))
        return await handler(event, data)
