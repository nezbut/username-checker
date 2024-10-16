from dishka import AsyncContainer, Provider, make_async_container

from username_checker.common.settings import Settings
from username_checker.infrastructure.di.broker import get_broker_providers
from username_checker.infrastructure.di.clients import get_clients_providers
from username_checker.infrastructure.di.database import get_database_providers
from username_checker.infrastructure.di.logs import get_logging_providers
from username_checker.infrastructure.di.settings import get_settings_providers
from username_checker.infrastructure.di.taskiq_provider import get_taskiq_providers
from username_checker.tgbot.di.bot import get_bot_providers
from username_checker.tgbot.di.i18n import get_i18n_bot_providers
from username_checker.tgbot.di.throttling import get_throttling_providers


def get_providers() -> list[Provider]:
    """Returns a list of providers for the main infrastructure components."""
    return [
        *get_logging_providers(),
        *get_settings_providers(),
        *get_database_providers(),
        *get_taskiq_providers(),
        *get_bot_providers(),
        *get_clients_providers(),
        *get_broker_providers(),
        *get_i18n_bot_providers(),
        *get_throttling_providers(),
    ]


def create_container(settings: Settings) -> AsyncContainer:
    """Creates an asynchronous container instance."""
    return make_async_container(*get_providers(), context={Settings: settings})
