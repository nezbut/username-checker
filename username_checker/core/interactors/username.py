from uuid import UUID

from username_checker.core.entities.subscription import Interval, Subscription, SubscriptionIdGenerator
from username_checker.core.entities.user import User
from username_checker.core.entities.username import Username, UsernameIdGenerator
from username_checker.core.interfaces import username as username_interfaces
from username_checker.core.interfaces.commiter import Commiter
from username_checker.core.interfaces.scheduler import Scheduler
from username_checker.core.interfaces.subscription import SubscriptionDeleter, SubscriptionUpserter
from username_checker.core.interfaces.uploader import UsernameUploader
from username_checker.core.services import subscription as sub_services
from username_checker.core.services import username as username_services


class GetUsername:

    """Class getting a username."""

    def __init__(
            self,
            checker: username_interfaces.UsernameChecker,
            id_generator: UsernameIdGenerator,
            getter: username_interfaces.UsernameGetter,
            upserter: username_interfaces.UsernameUpserter,
            commiter: Commiter,
    ) -> None:
        self.checker = checker
        self.id_generator = id_generator
        self.upserter = upserter
        self.getter = getter
        self.commiter = commiter

    async def __call__(self, value: str) -> Username:
        """
        Retrieves a username by its value. If the username does not exist,

        it creates a new one, checks its status, and saves it to the database.

        :param value: The value of the username to retrieve.
        :type value: str
        :return: The retrieved or created username.
        :rtype: Username
        """
        username = await username_services.get_by_value(value, self.getter)
        if username is None:
            username = Username(
                id=self.id_generator(),
                value=value,
            )
            saved_username = await username_services.upsert_username(username, self.upserter)
            await self.commiter.commit()
            return saved_username
        return username


class CheckUsername:

    """Class checking a username status."""

    def __init__(
            self,
            checker: username_interfaces.UsernameChecker,
            upserter: username_interfaces.UsernameUpserter,
            commiter: Commiter,
    ) -> None:
        self.checker = checker
        self.upserter = upserter
        self.commiter = commiter

    async def __call__(self, username: Username) -> Username:
        """
        Check username status

        :param username: The username to be checked.
        :type username: Username
        :return: username with new status
        :rtype: Username
        """
        status = await username_services.check_username(username, self.checker)
        if username.status != status:
            username.status = status
            username = await username_services.upsert_username(username, self.upserter)
            await self.commiter.commit()
        return username


class SubscribeCheckUsername:

    """A class responsible for subscribing to check usernames."""

    def __init__(
            self,
            scheduler: Scheduler,
            id_generator: SubscriptionIdGenerator,
            upserter: SubscriptionUpserter,
            commiter: Commiter,
    ) -> None:
        self.scheduler = scheduler
        self.id_generator = id_generator
        self.upserter = upserter
        self.commiter = commiter

    async def __call__(self, subscriber: User, username: Username, interval: Interval) -> str:
        """
        Subscribes a user to check a username at a specified interval.

        :param subscriber: The user subscribing to the check.
        :type subscriber: User
        :param username: The username to be checked.
        :type username: str
        :param interval: The interval at which the username should be checked.
        :type interval: Interval
        :return: The result of the scheduled username check.
        :rtype: str
        """
        subscription = Subscription(
            id=self.id_generator(),
            username=username,
            interval=interval,
            subscriber=subscriber,
        )
        sub = await sub_services.upsert_subscription(subscription, self.upserter)
        schedule_check_id = await self.scheduler.schedule_check_username(sub)
        await self.commiter.commit()
        return schedule_check_id


class UnsubscribeCheckUsername:

    """A class responsible for unsubscribing from check usernames."""

    def __init__(self, scheduler: Scheduler, deleter: SubscriptionDeleter, commiter: Commiter) -> None:
        self.scheduler = scheduler
        self.deleter = deleter
        self.commiter = commiter

    async def __call__(self, subscription_id: UUID) -> None:
        """
        Unsubscribe a username check.

        :param subscription_id: Identifier of the subscription.
        :type subscription_id: UUID
        """
        await sub_services.delete_subscription(subscription_id, self.deleter)
        await self.scheduler.unschedule_check_username(subscription_id)
        await self.commiter.commit()


class UploadAvailableUsernames:

    """A class responsible for uploading available usernames for user."""

    def __init__(self, uploader: UsernameUploader, getter: username_interfaces.UsernameGetter) -> None:
        self.uploader = uploader
        self.getter = getter

    async def __call__(self, user: User) -> str:
        """
        Uploads available usernames.

        :param usernames: List of available usernames.
        :type usernames: list[str]
        """
        usernames = await username_services.get_available_usernames_for_user(user, self.getter)
        return await self.uploader.upload(usernames)
