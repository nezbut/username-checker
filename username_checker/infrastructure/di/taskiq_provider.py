
from dishka import Provider, Scope, provide
from taskiq import AsyncBroker, AsyncResultBackend

from username_checker.infrastructure.tkq.constants import taskiq_broker


class TaskiqProvider(Provider):

    """Provider for Taskiq."""

    scope = Scope.APP

    @provide
    async def get_broker(self) -> AsyncBroker:
        """Get the broker instance."""
        return taskiq_broker

    @provide
    async def get_result_backend(self) -> AsyncResultBackend:
        """Get the result backend instance."""
        return taskiq_broker.result_backend


def get_taskiq_providers() -> list[Provider]:
    """Returns a list of taskiq providers for di."""
    return [
        TaskiqProvider(),
    ]
