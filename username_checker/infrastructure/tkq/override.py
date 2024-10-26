from typing import Any

from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from dishka.integrations.taskiq import setup_dishka
from nats.js.api import ConsumerConfig, StreamConfig
from taskiq_nats import PullBasedJetStreamBroker, PushBasedJetStreamBroker  # type: ignore[import-untyped]

from username_checker.common.settings import Settings
from username_checker.core.interactors import username
from username_checker.infrastructure.di.broker import get_broker_providers
from username_checker.infrastructure.di.checker import get_username_checkers_providers
from username_checker.infrastructure.di.clients import get_clients_providers
from username_checker.infrastructure.di.database import get_database_providers
from username_checker.infrastructure.di.logs import get_logging_providers
from username_checker.infrastructure.di.proxy import get_proxy_providers
from username_checker.infrastructure.di.settings import get_settings_providers
from username_checker.infrastructure.di.uploader import get_uploader_providers
from username_checker.tgbot.di.bot import get_bot_providers
from username_checker.tgbot.di.i18n import get_i18n_bot_providers
from username_checker.tgbot.di.throttling import get_throttling_providers


class _OverrideProvider(Provider):

    check_username = provide(username.CheckUsername, scope=Scope.REQUEST)


def _create_override_container(settings: Settings) -> AsyncContainer:
    providers = [
        *get_database_providers(),
        *get_settings_providers(),
        *get_bot_providers(),
        *get_clients_providers(),
        *get_broker_providers(),
        *get_i18n_bot_providers(),
        *get_logging_providers(),
        *get_throttling_providers(),
        *get_proxy_providers(),
        *get_username_checkers_providers(),
        *get_uploader_providers(),
        _OverrideProvider(),
    ]
    return make_async_container(*providers, context={Settings: settings})


class PullBasedJetStreamBrokerDI(
    PullBasedJetStreamBroker,  # type: ignore[no-any-unimported]
):

    """
    JetStream broker for pull based message consumption.

    It's named `pull` based because consumer requests messages,
    not NATS server sends them.
    """

    def __init__(
        self,
        settings: Settings,
        servers: str | list[str],
        subject: str = "taskiq_tasks",
        stream_name: str = "taskiq_jetstream",
        queue: str | None = None,
        durable: str = "taskiq_durable",
        stream_config: StreamConfig | None = None,
        consumer_config: ConsumerConfig | None = None,
        pull_consume_batch: int = 1,
        pull_consume_timeout: float | None = None,
        **connection_kwargs: Any,
    ) -> None:
        self.settings = settings
        super().__init__(servers, subject, stream_name, queue, durable, stream_config,
                         consumer_config, pull_consume_batch, pull_consume_timeout, **connection_kwargs)

    async def startup(self) -> None:
        """
        Startup event handler.

        It simply connects to NATS cluster, and
        setup JetStream.
        """
        container = _create_override_container(self.settings)
        await super().startup()
        setup_dishka(container, self)


class PushBasedJetStreamBrokerDI(
    PushBasedJetStreamBroker,  # type: ignore[no-any-unimported]
):

    """
    JetStream broker for push based message consumption.

    It's named `push` based because nats server push messages to
    the consumer, not consumer requests them.
    """

    def __init__(
        self,
        settings: Settings,
        servers: str | list[str],
        subject: str = "taskiq_tasks",
        stream_name: str = "taskiq_jetstream",
        queue: str | None = None,
        durable: str = "taskiq_durable",
        stream_config: StreamConfig | None = None,
        consumer_config: ConsumerConfig | None = None,
        pull_consume_batch: int = 1,
        pull_consume_timeout: float | None = None,
        **connection_kwargs: Any,
    ) -> None:
        self.settings = settings
        super().__init__(servers, subject, stream_name, queue, durable, stream_config,
                         consumer_config, pull_consume_batch, pull_consume_timeout, **connection_kwargs)

    async def startup(self) -> None:
        """
        Startup event handler.

        It simply connects to NATS cluster, and
        setup JetStream.
        """
        container = _create_override_container(self.settings)
        await super().startup()
        setup_dishka(container, self)
