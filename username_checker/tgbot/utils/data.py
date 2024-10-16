from collections.abc import Callable
from typing import Any, Concatenate, TypedDict

from aiogram import Bot, Router, types
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from dishka import AsyncContainer
from fluentogram import TranslatorHub, TranslatorRunner
from structlog.stdlib import BoundLogger

from username_checker.common.settings import Settings
from username_checker.common.settings.models import broker, db, logs, telegram
from username_checker.infrastructure.clients.cache.base import BaseCacheClient
from username_checker.infrastructure.database.rdb.holder import HolderDAO
from username_checker.tgbot.throttling.manager import ThrottleManager

I18NGetter = Callable[Concatenate[...], str]


class AiogramMiddlewareData(TypedDict, total=False):

    """A dictionary containing middleware data for Aiogram."""

    event_from_user: types.User
    event_chat: types.Chat
    bot: Bot
    fsm_storage: BaseStorage
    state: FSMContext
    raw_state: Any
    handler: HandlerObject
    event_update: types.Update
    event_router: Router


class SettingsMiddlewareData(TypedDict, total=False):

    """A dictionary containing middleware data for settings."""

    settings: Settings

    broker_settings: broker.BrokerSettings
    nats_settings: broker.NatsSettings
    tasks_nats_settings: broker.TasksNatsSettings

    db_settings: db.DBSettings
    rdb_settings: db.RDBSettings
    redis_settings: db.RedisSettings
    tasks_redis_settings: db.TasksRedisSettings
    result_backend: db.TasksResultBackend

    logging_settings: logs.LoggingSettings

    telegram_settings: telegram.TelegramBot
    fsm_storage_settings: telegram.FSMStorageSettings
    admin_settings: telegram.AdminSettings


class MiddlewareData(AiogramMiddlewareData, SettingsMiddlewareData, total=False):

    """Middleware data for aiogram."""

    dishka_container: AsyncContainer
    holder_dao: HolderDAO
    cache: BaseCacheClient
    throttle_manager: ThrottleManager

    translator_hub: TranslatorHub
    i18n: TranslatorRunner
    i18n_getter: I18NGetter

    logger: BoundLogger
