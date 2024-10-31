from typing import Protocol
from uuid import UUID

from username_checker.core.entities.subscription import Subscription


class Scheduler(Protocol):

    """A class representing a scheduler."""

    async def schedule_check_username(self, subscription: Subscription) -> str:
        """
        Schedules a username check from a subscription.

        :param subscription: The subscription.
        :type subscription: Subscription
        :return: Identifier of the scheduled check.
        """
        ...

    async def unschedule_check_username(self, subscription_id: UUID) -> None:
        """
        Unscheduled a username check.

        :param subscription_id: Identifier of the subscription.
        :type subscription_id: UUID
        """
        ...
