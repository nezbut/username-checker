from username_checker.core.entities.subscription import Subscription
from username_checker.core.interfaces.scheduler import Scheduler
from username_checker.core.interfaces.username import UsernameChecker


class CheckUsername:

    """Class checking if a username is valid."""

    def __init__(self, checker: UsernameChecker) -> None:
        self.checker = checker

    async def __call__(self, username: str) -> bool:
        """
        Checks if a given username is valid.

        :param username: The username to be checked.
        :return: True if the username is valid, False otherwise.
        """
        return await self.checker.check(username)


class SubscribeCheckUsername:

    """Class subscribing to a username check."""

    def __init__(self, scheduler: Scheduler) -> None:
        self.scheduler = scheduler

    async def __call__(self, subscription: Subscription) -> str:
        """
        Schedules a username check based on the provided subscription.

        :param subscription: The subscription containing the username to be checked.
        :return: The result of the scheduled username check.
        """
        return await self.scheduler.schedule_check_username(subscription)
