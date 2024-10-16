from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from nats.js.api import KeyValueConfig

from username_checker.common.settings.models.security import SecretStr


class FSMStorageType(Enum):

    """An enumeration of FSM storage types."""

    MEMORY = "memory"
    NATS = "nats"
    REDIS = "redis"


@dataclass
class BotProperties:

    """A class representing the bot properties."""

    parse_mode: Optional[str] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_sending_without_reply: Optional[bool] = None
    link_preview_is_disabled: Optional[bool] = None
    link_preview_prefer_small_media: Optional[bool] = None
    link_preview_prefer_large_media: Optional[bool] = None
    link_preview_show_above_text: Optional[bool] = None
    show_caption_above_media: Optional[bool] = None


@dataclass
class NatsFSMStorageSettings:

    """A class representing the settings for the Nats FSM storage."""

    kv_states: KeyValueConfig = field(
        default_factory=lambda: KeyValueConfig("fsm_states_tgbot"),
    )
    kv_data: KeyValueConfig = field(
        default_factory=lambda: KeyValueConfig("fsm_data_tgbot"),
    )
    create_nats_kv_buckets: bool = False


@dataclass
class RedisFSMStorageSettings:

    """A class representing the settings for the Redis FSM storage."""

    db: int = 2
    connection_kwargs: Optional[dict[str, Any]] = None


@dataclass
class FSMStorageSettings:

    """A class representing the settings for the FSM storage."""

    storage_type: FSMStorageType = FSMStorageType.NATS
    nats: NatsFSMStorageSettings = field(
        default_factory=lambda: NatsFSMStorageSettings(),
    )
    redis: RedisFSMStorageSettings = field(
        default_factory=lambda: RedisFSMStorageSettings(),
    )


@dataclass
class AdminSettings:

    """A class representing the settings for the admin."""

    superusers: list[int] = field(default_factory=list)


@dataclass
class TelegramBot:

    """A class representing a Telegram bot settings."""

    properties: BotProperties
    admin: AdminSettings
    fsm_storage: FSMStorageSettings
    token: Optional[SecretStr] = None
    throttling_rate_limit: float = 0.5

    def create_bot_instance(self) -> Bot:
        """
        Creates a Telegram bot instance based on the provided settings.

        :return: A Telegram bot instance.
        :rtype: Bot
        """
        if self.token is None:
            raise OSError("Telegram bot token is not set")
        return Bot(
            token=self.token.value,
            default=DefaultBotProperties(
                parse_mode=self.properties.parse_mode,
                disable_notification=self.properties.disable_notification,
                protect_content=self.properties.protect_content,
                allow_sending_without_reply=self.properties.allow_sending_without_reply,
                link_preview_is_disabled=self.properties.link_preview_is_disabled,
                link_preview_prefer_small_media=self.properties.link_preview_prefer_small_media,
                link_preview_prefer_large_media=self.properties.link_preview_prefer_large_media,
                link_preview_show_above_text=self.properties.link_preview_show_above_text,
                show_caption_above_media=self.properties.show_caption_above_media,
            ),
        )
