from collections.abc import Callable
from typing import Any, Concatenate, TypedDict

from aiogram import Bot, Router, types
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from aiogram_dialog.api.entities import Context, Stack
from aiogram_dialog.api.protocols import BgManagerFactory, DialogManager
from aiogram_dialog.context.storage import StorageProxy
from dishka import AsyncContainer
from fluentogram import TranslatorHub, TranslatorRunner
from structlog.stdlib import BoundLogger

from username_checker.common.settings import Settings
from username_checker.common.settings.models import broker, cache, db, logs, telegram
from username_checker.core.interactors import subscription as sub_interactors
from username_checker.core.interactors import username as username_interactors
from username_checker.infrastructure.clients.cache.base import BaseCacheClient
from username_checker.infrastructure.database.rdb.holder import HolderDAO
from username_checker.infrastructure.proxy.user import CurrentUserProxy, UserProxy
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


class DialogMiddlewareData(TypedDict, total=False):

    """A dictionary containing middleware data for aiogram dialog."""

    dialog_manager: DialogManager
    aiogd_storage_proxy: StorageProxy
    aiogd_stack: Stack
    aiogd_context: Context


class SettingsMiddlewareData(TypedDict, total=False):

    """A dictionary containing middleware data for settings."""

    settings: Settings

    broker_settings: broker.BrokerSettings
    nats_settings: broker.NatsSettings
    tasks_nats_settings: broker.TasksNatsSettings

    cache_settings: cache.CacheSettings
    cache_client_settings: cache.CacheClientSettings
    ttl_cache_client_settings: cache.TTLCacheClientSettings

    db_settings: db.DBSettings
    rdb_settings: db.RDBSettings
    redis_settings: db.RedisSettings
    tasks_redis_settings: db.TasksRedisSettings
    result_backend: db.TasksResultBackend
    schedule_source: db.TasksScheduleSource

    logging_settings: logs.LoggingSettings

    telegram_settings: telegram.TelegramBot
    fsm_storage_settings: telegram.FSMStorageSettings
    admin_settings: telegram.AdminSettings


class InteractorsMiddlewareData(TypedDict, total=False):

    """A dictionary containing middleware data for interactors."""

    get_user_subscriptions: sub_interactors.GetUserSubscriptions

    get_username: username_interactors.GetUsername
    check_username: username_interactors.CheckUsername
    subscribe_check_username: username_interactors.SubscribeCheckUsername
    unsubscribe_check_username: username_interactors.UnsubscribeCheckUsername
    upload_available_usernames: username_interactors.UploadAvailableUsernames


class MiddlewareData(AiogramMiddlewareData, DialogMiddlewareData, SettingsMiddlewareData, InteractorsMiddlewareData, total=False):

    """Middleware data for aiogram."""

    dishka_container: AsyncContainer
    holder_dao: HolderDAO
    bg_manager_factory: BgManagerFactory
    cache: BaseCacheClient
    throttle_manager: ThrottleManager
    user_proxy: UserProxy
    current_user: CurrentUserProxy

    translator_hub: TranslatorHub
    i18n: TranslatorRunner
    i18n_getter: I18NGetter

    logger: BoundLogger
