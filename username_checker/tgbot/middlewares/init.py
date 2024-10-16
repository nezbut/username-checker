from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from username_checker.common.settings import Settings
from username_checker.infrastructure.clients.cache.base import BaseCacheClient
from username_checker.infrastructure.database.rdb.holder import HolderDAO
from username_checker.tgbot.throttling.manager import ThrottleManager
from username_checker.tgbot.utils.data import MiddlewareData


class InitMiddleware(BaseMiddleware):

    """Init middleware."""

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        self.settings = settings

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """Init middleware."""
        container = data["dishka_container"]

        data["settings"] = self.settings

        data["broker_settings"] = self.settings.broker
        data["nats_settings"] = self.settings.broker.nats
        data["tasks_nats_settings"] = self.settings.broker.nats.tasks

        data["db_settings"] = self.settings.db
        data["rdb_settings"] = self.settings.db.rdb
        data["redis_settings"] = self.settings.db.redis
        data["tasks_redis_settings"] = self.settings.db.redis.tasks
        data["result_backend"] = self.settings.db.redis.tasks.result_backend

        data["logging_settings"] = self.settings.logging

        data["telegram_settings"] = self.settings.bot
        data["fsm_storage_settings"] = self.settings.bot.fsm_storage
        data["admin_settings"] = self.settings.bot.admin

        data["holder_dao"] = await container.get(HolderDAO)
        data["cache"] = await container.get(BaseCacheClient)
        data["throttle_manager"] = await container.get(ThrottleManager)

        return await handler(event, data)
