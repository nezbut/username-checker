from typing import Optional
from uuid import UUID

from username_checker.core.entities.subscription import Subscription
from username_checker.core.entities.user import User
from username_checker.core.entities.username import Username
from username_checker.core.interfaces import subscription as interfaces


async def upsert_subscription(subscription: Subscription, upserter: interfaces.SubscriptionUpserter) -> Subscription:
    """
    Upserts a subscription using the provided upserter.

    :param subscription: The subscription to be upserted.
    :type subscription: Subscription
    :param upserter: The upserter to perform the upsert operation.
    :type upserter: SubscriptionUpserter
    :return: The upserted subscription.
    :rtype: Subscription
    """
    return await upserter.upsert(subscription)


async def delete_subscription(subscription_id: UUID, deleter: interfaces.SubscriptionDeleter) -> bool:
    """
    Deletes a subscription using the provided deleter.

    :param subscription_id: The ID of the subscription to be deleted.
    :type subscription_id: UUID
    :param deleter: The deleter to perform the deletion operation.
    :type deleter: SubscriptionDeleter
    :return: bool
    """
    return await deleter.delete(subscription_id)


async def get_by_username(username: Username, getter: interfaces.SubscriptionGetter) -> Optional[Subscription]:
    """
    Gets a subscription by username using the provided getter.

    :param username: The username of the subscription.
    :type username: Username
    :param getter: The getter to perform the get operation.
    :type getter: SubscriptionGetter
    :return: The subscription.
    :rtype: Subscription
    """
    return await getter.get_by_username(username)


async def get_by_id(subscription_id: UUID, getter: interfaces.SubscriptionGetter) -> Optional[Subscription]:
    """
    Gets a subscription by ID using the provided getter.

    :param subscription_id: The ID of the subscription.
    :type subscription_id: UUID
    :param getter: The getter to perform the get operation.
    :type getter: SubscriptionGetter
    :return: The subscription.
    :rtype: Subscription
    """
    return await getter.get_by_id(subscription_id)


async def get_subscriptions(getter: interfaces.SubscriptionGetter, subscription_ids: Optional[list[UUID]] = None) -> list[Subscription]:
    """
    Gets all subscriptions or subscriptions by their IDs using the provided getter.

    :param subscription_ids: An optional list of subscription IDs.
    :type subscription_ids: Optional[list[UUID]]
    :param getter: The getter to perform the get operation.
    :type getter: SubscriptionGetter
    :return: A list of all subscriptions or subscriptions by their IDs.
    :rtype: list[Subscription]
    """
    return await getter.get_subscriptions(subscription_ids)


async def get_by_subscriber(subscriber: User, getter: interfaces.SubscriptionGetter) -> Optional[Subscription]:
    """
    Get subscription by a subscriber.

    :param subscriber: The user.
    :type subscriber: User
    :param getter: The getter to perform the get operation.
    :type getter: SubscriptionGetter
    :return: Subscription by a subscriber.
    :rtype: Subscription
    """
    return await getter.get_by_subscriber(subscriber)
