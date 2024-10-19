from typing import Optional, Protocol
from uuid import UUID

from username_checker.core.entities.subscription import Subscription
from username_checker.core.entities.user import User
from username_checker.core.entities.username import Username


class SubscriptionDeleter(Protocol):

    """A protocol for deleting subscriptions."""

    async def delete(self, subscription_id: UUID) -> bool:
        """
        Deletes a subscription.

        :param subscription_id: The ID of the subscription to be deleted.
        :type subscription_id: UUID
        :return: bool
        """
        ...


class SubscriptionUpserter(Protocol):

    """A protocol for upserting subscriptions."""

    async def upsert(self, subscription: Subscription) -> Subscription:
        """
        Upserts a subscription.

        :param subscription: The subscription to be upserted.
        :type subscription: Subscription
        :return: The upserted subscription.
        :rtype: Subscription
        """
        ...


class SubscriptionGetter(Protocol):

    """A protocol for getting subscriptions."""

    async def get_by_username(self, username: Username) -> Subscription:
        """
        Gets a subscription by username.

        :param username: The username of the subscription.
        :type username: Username
        :return: The subscription.
        :rtype: Subscription
        """
        ...

    async def get_by_id(self, subscription_id: UUID) -> Subscription:
        """
        Gets a subscription by ID.

        :param subscription_id: The ID of the subscription.
        :type subscription_id: UUID
        :return: The subscription.
        :rtype: Subscription
        """
        ...

    async def get_by_user(self, user: User) -> list[Subscription]:
        """
        Gets all subscriptions by a user.

        :param user: The user.
        :type user: User
        :return: A list of all subscriptions by a user.
        :rtype: list[Subscription]
        """
        ...

    async def get_subscriptions(self, subscription_ids: Optional[list[UUID]] = None) -> list[Subscription]:
        """
        Gets all subscriptions or subscriptions by their IDs.

        :param subscription_ids: An optional list of subscription IDs.
        :return: A list of all subscriptions or subscriptions by their IDs.
        """
        ...
