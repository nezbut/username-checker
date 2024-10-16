from dishka import Provider, Scope, provide

from username_checker.tgbot.throttling.manager import ThrottleManager


class ThrottlingProvider(Provider):

    """A provider class Throttling."""

    scope = Scope.APP

    throttle_manager = provide(ThrottleManager)


def get_throttling_providers() -> list[Provider]:
    """Returns a list of providers for Throttling."""
    return [
        ThrottlingProvider(),
    ]
