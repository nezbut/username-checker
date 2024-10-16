from dishka import Provider, Scope, from_context, provide

from username_checker.common.settings import Settings
from username_checker.common.settings.models import broker, cache, db, logs
from username_checker.common.settings.models import telegram as tg


class SettingsProvider(Provider):

    """Provider for Settings"""

    scope = Scope.APP

    settings = from_context(Settings)


class BotSettingsProvider(Provider):

    """Provider for Bot Settings"""

    scope = Scope.APP

    @provide
    def get_bot_settings(self, settings: Settings) -> tg.TelegramBot:
        """Provides the Telegram bot settings from the given settings."""
        return settings.bot

    @provide
    def get_fsm_storage_settings(self, bot_settings: tg.TelegramBot) -> tg.FSMStorageSettings:
        """Get the FSM storage settings from the given bot settings."""
        return bot_settings.fsm_storage

    @provide
    def get_nats_fsm_storage_settings(self, fsm_settings: tg.FSMStorageSettings) -> tg.NatsFSMStorageSettings:
        """Get the Nats FSM storage settings from the given bot settings."""
        return fsm_settings.nats

    @provide
    def get_redis_fsm_storage_settings(self, fsm_settings: tg.FSMStorageSettings) -> tg.RedisFSMStorageSettings:
        """Get the Redis FSM storage settings from the given bot settings."""
        return fsm_settings.redis


class LoggingSettingsProvider(Provider):

    """Provider for Logging Settings"""

    scope = Scope.APP

    @provide
    def get_logging_settings(self, settings: Settings) -> logs.LoggingSettings:
        """Provides the logging settings from the given settings."""
        return settings.logging


class DBSettingsProvider(Provider):

    """Provider for DataBase Settings"""

    scope = Scope.APP

    @provide
    def get_db_settings(self, settings: Settings) -> db.DBSettings:
        """Provides the database settings from the given settings."""
        return settings.db

    @provide
    def get_rdb_settings(self, db_settings: db.DBSettings) -> db.RDBSettings:
        """Provides the relational database settings from the given database settings."""
        return db_settings.rdb

    @provide
    def get_redis_settings(self, db_settings: db.DBSettings) -> db.RedisSettings:
        """Provides the Redis settings from the given database settings."""
        return db_settings.redis

    @provide
    def get_redis_tasks_settings(self, redis_settings: db.RedisSettings) -> db.TasksRedisSettings:
        """Get the Redis tasks settings from the given Redis settings."""
        return redis_settings.tasks


class BrokerSettingsProvider(Provider):

    """Provider for Broker Settings"""

    scope = Scope.APP

    @provide
    def get_broker_settings(self, settings: Settings) -> broker.BrokerSettings:
        """Provide the broker settings from the given settings."""
        return settings.broker

    @provide
    def get_nats_settings(self, broker_settings: broker.BrokerSettings) -> broker.NatsSettings:
        """Provides the NATS settings from the given broker settings."""
        return broker_settings.nats

    @provide
    def get_nats_tasks_settings(self, nats_settings: broker.NatsSettings) -> broker.TasksNatsSettings:
        """Get the NATS tasks settings from the given NATS settings."""
        return nats_settings.tasks


class CacheSettingsProvider(Provider):

    """Provider for Cache Settings."""

    scope = Scope.APP

    @provide
    def get_cache_settings(self, settings: Settings) -> cache.CacheSettings:
        """Provides the cache settings from the given settings."""
        return settings.cache

    @provide
    def get_cache_client_settings(self, cache_settings: cache.CacheSettings) -> cache.CacheClientSettings:
        """Provides the cache client settings from the given cache settings."""
        return cache_settings.client

    @provide
    def get_ttl_cache(self, client_settings: cache.CacheClientSettings) -> cache.TTLCacheClientSettings:
        """Provides the TTL cache settings from the given cache client settings."""
        return client_settings.ttl_cache


def get_settings_providers() -> list[Provider]:
    """Returns a list of settings providers for di."""
    return [
        SettingsProvider(),
        BotSettingsProvider(),
        LoggingSettingsProvider(),
        DBSettingsProvider(),
        BrokerSettingsProvider(),
        CacheSettingsProvider(),
    ]
