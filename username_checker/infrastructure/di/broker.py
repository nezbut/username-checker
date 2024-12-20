from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from nats import connect
from nats.aio.client import Client
from nats.js import JetStreamContext

from username_checker.common.log.configuration import LoggerName
from username_checker.common.log.installer import LoggersInstaller
from username_checker.common.settings.models.broker import NatsSettings


class NatsProvider(Provider):

    """Provider for Nats."""

    scope = Scope.APP

    @provide
    async def get_client(self, settings: NatsSettings, logging: LoggersInstaller) -> AsyncIterable[Client]:
        """Get Nats Client"""
        logger = logging.get_logger(LoggerName.BROKER)
        servers = [server.make_uri().value for server in settings.servers]
        await logger.ainfo("Trying to connect to nats servers: %s", servers)
        async with await connect(servers) as nc:
            await logger.ainfo("Connected to nats servers: %s", servers)
            yield nc

    @provide
    async def get_js(self, client: Client) -> JetStreamContext:
        """Get JetStream context"""
        return client.jetstream()


def get_broker_providers() -> list[Provider]:
    """Returns a nats providers for di."""
    return [
        NatsProvider(),
    ]
