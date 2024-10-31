from uuid import uuid4

from dishka import Provider, Scope, provide

from username_checker.core.entities.subscription import SubscriptionIdGenerator
from username_checker.core.entities.username import UsernameIdGenerator
from username_checker.core.interactors import subscription, username


class InteractorsProvider(Provider):

    """Provider for interactors."""

    scope = Scope.REQUEST

    get_user_subscriptions = provide(subscription.GetUserSubscriptions)

    get_username = provide(username.GetUsername)
    check_username = provide(username.CheckUsername)
    subscribe_check_username = provide(username.SubscribeCheckUsername)
    unsubscribe_check_username = provide(username.UnsubscribeCheckUsername)
    upload_available_usernames = provide(username.UploadAvailableUsernames)


class IdGeneratorsProvider(Provider):

    """Provider for id generators."""

    scope = Scope.APP

    @provide()
    async def get_username_id_generator(self) -> UsernameIdGenerator:
        """Returns a username id generator."""
        return uuid4

    @provide()
    async def get_subscription_id_generator(self) -> SubscriptionIdGenerator:
        """Returns a subscription id generator."""
        return uuid4


def get_interactors_providers() -> list[Provider]:
    """Returns a list of interactors providers for di."""
    return [
        IdGeneratorsProvider(),
        InteractorsProvider(),
    ]
