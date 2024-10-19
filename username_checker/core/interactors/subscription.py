from username_checker.core.entities.subscription import Subscription
from username_checker.core.entities.user import User
from username_checker.core.interfaces.subscription import SubscriptionGetter
from username_checker.core.services import subscription as sub_services


class GetUserSubscriptions:

    """A class responsible for getting user subscriptions."""

    def __init__(self, getter: SubscriptionGetter):
        self.getter = getter

    async def __call__(self, user: User) -> list[Subscription]:
        """
        Retrieves a list of subscriptions associated with a given user.

        :param user: The user whose subscriptions are to be retrieved.
        :type user: User
        :return: A list of subscriptions associated with the user.
        :rtype: list[Subscription]
        """
        return await sub_services.get_by_user(user, self.getter)
