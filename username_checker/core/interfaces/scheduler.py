from typing import Protocol

from username_checker.core.entities.subscription import Subscription


class Scheduler(Protocol):

    """A class representing a scheduler."""

    async def schedule_check_username(self, subscription: Subscription) -> str:
        """
        Schedules a username check.

        :param username: The username to be checked.
        :return: The result of the scheduled username check.
        """
        ...
