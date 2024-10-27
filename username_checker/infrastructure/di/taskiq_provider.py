
from dishka import Provider, Scope, provide
from taskiq import AsyncBroker, AsyncResultBackend, ScheduleSource

from username_checker.core.interfaces.scheduler import Scheduler
from username_checker.infrastructure.tkq.constants import schedule_source, taskiq_broker
from username_checker.infrastructure.tkq.scheduler import SchedulerImpl


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

    @provide
    async def get_schedule_source(self) -> ScheduleSource:
        """Get the schedule source instance."""
        return schedule_source


class SchedulerProvider(Provider):

    """Provider for Scheduler."""

    scope = Scope.APP

    scheduler = provide(SchedulerImpl, provides=Scheduler)


def get_taskiq_providers() -> list[Provider]:
    """Returns a list of taskiq providers for di."""
    return [
        TaskiqProvider(),
        SchedulerProvider(),
    ]
