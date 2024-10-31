from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog.api.protocols import BgManagerFactory

from username_checker.common.settings import Settings
from username_checker.infrastructure.clients.cache.base import BaseCacheClient
from username_checker.infrastructure.database.rdb.holder import HolderDAO
from username_checker.infrastructure.proxy.user import UserProxy
from username_checker.tgbot.throttling.manager import ThrottleManager
from username_checker.tgbot.utils.data import MiddlewareData


class InitMiddleware(BaseMiddleware):

    """Init middleware."""

    def __init__(
        self,
        bg_manager_factory: BgManagerFactory,
        settings: Settings,
    ) -> None:
        self.bg_manager_factory = bg_manager_factory
        self.settings = settings

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """Init middleware."""
        container = data["dishka_container"]

        data["bg_manager_factory"] = self.bg_manager_factory
        data["settings"] = self.settings

        data["broker_settings"] = self.settings.broker
        data["nats_settings"] = self.settings.broker.nats
        data["tasks_nats_settings"] = self.settings.broker.nats.tasks

        data["cache_settings"] = self.settings.cache
        data["cache_client_settings"] = self.settings.cache.client
        data["ttl_cache_client_settings"] = self.settings.cache.client.ttl_cache

        data["db_settings"] = self.settings.db
        data["rdb_settings"] = self.settings.db.rdb
        data["redis_settings"] = self.settings.db.redis
        data["tasks_redis_settings"] = self.settings.db.redis.tasks
        data["result_backend"] = self.settings.db.redis.tasks.result_backend
        data["schedule_source"] = self.settings.db.redis.tasks.schedule_source

        data["logging_settings"] = self.settings.logging

        data["telegram_settings"] = self.settings.bot
        data["fsm_storage_settings"] = self.settings.bot.fsm_storage
        data["admin_settings"] = self.settings.bot.admin

        data["holder_dao"] = await container.get(HolderDAO)
        data["cache"] = await container.get(BaseCacheClient)
        data["throttle_manager"] = await container.get(ThrottleManager)
        data["user_proxy"] = UserProxy(
            dao=data["holder_dao"].user,
            cache=data["cache"],
            commiter=data["holder_dao"],
        )

        return await handler(event, data)
