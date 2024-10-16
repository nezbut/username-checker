from dataclasses import dataclass
from functools import lru_cache
from typing import Any, TypeVar

from adaptix import Retort
from adaptix.load_error import AggregateLoadError, NoRequiredFieldsLoadError

from username_checker.common.settings.dynaconf_config import dynaconf_settings
from username_checker.common.settings.models.broker import BrokerSettings
from username_checker.common.settings.models.cache import CacheSettings
from username_checker.common.settings.models.db import DBSettings
from username_checker.common.settings.models.logs import LoggingSettings
from username_checker.common.settings.models.telegram import TelegramBot

_DataClass = TypeVar("_DataClass")

_settings_retort = Retort()


@dataclass
class Settings:

    """A class representing the application settings."""

    bot: TelegramBot
    logging: LoggingSettings
    db: DBSettings
    broker: BrokerSettings
    cache: CacheSettings

    @classmethod
    @lru_cache
    def from_dynaconf(cls) -> "Settings":
        """
        A class method that creates a Settings instance from dynaconf settings.

        It loads the settings from dynaconf and returns a Settings instance with the loaded settings.

        Returns :
            Settings: A Settings instance
        """
        bot = cls._get_settings("bot", TelegramBot)
        db = cls._get_settings("db", DBSettings)
        broker = cls._get_settings("broker", BrokerSettings)
        logs = cls._get_settings("logging", LoggingSettings)
        cache = cls._get_settings("cache", CacheSettings)

        return cls(
            bot=bot,
            logging=logs,
            db=db,
            broker=broker,
            cache=cache,
        )

    @staticmethod
    def _get_settings(key: str, class_: type[_DataClass]) -> _DataClass:
        key_settings: dict[str, Any] = dynaconf_settings.get(key) or {}
        try:
            settings = _settings_retort.load(key_settings, class_)
        except AggregateLoadError as e:
            try:
                exc: NoRequiredFieldsLoadError = next(
                    exception for exception in e.exceptions
                    if isinstance(exception, NoRequiredFieldsLoadError)
                )
                key_settings.update({key_: {} for key_ in exc.fields})
                settings = _settings_retort.load(key_settings, class_)
            except StopIteration:
                raise e from e
        return settings
