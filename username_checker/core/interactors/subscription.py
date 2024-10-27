from typing import Optional

from username_checker.core.entities.subscription import Subscription
from username_checker.core.entities.user import User
from username_checker.core.interfaces.subscription import SubscriptionGetter
from username_checker.core.services import subscription as sub_services


class GetUserSubscriptions:

    """A class responsible for getting user subscriptions."""

    def __init__(self, getter: SubscriptionGetter):
        self.getter = getter

    async def __call__(self, subscriber: User) -> Optional[Subscription]:
        """
        Retrieves a list of subscriptions associated with a given user.

        :param subscriber: The subscriber whose subscriptions are to be retrieved.
        :type subscriber: User
        :return: A subscription.
        :rtype: Subscription
        """
        return await sub_services.get_by_subscriber(subscriber, self.getter)
