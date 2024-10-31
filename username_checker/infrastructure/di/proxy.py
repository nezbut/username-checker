from dishka import AnyOf, Provider, Scope, provide

from username_checker.core.interfaces import user as ui
from username_checker.infrastructure.proxy.user import UserProxy


class ProxyProvider(Provider):

    """Provider for proxies."""

    user_proxy_class = provide(UserProxy, scope=Scope.REQUEST, provides=AnyOf[
        UserProxy, ui.UserGetter, ui.UserUpdater, ui.UserUpserter,
    ])


def get_proxy_providers() -> list[Provider]:
    """Returns a list of proxy providers for di."""
    return [
        ProxyProvider(),
    ]
