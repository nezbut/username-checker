from typing import Any

from username_checker.core.interactors.subscription import GetUserSubscriptions
from username_checker.infrastructure.proxy.user import CurrentUserProxy


async def get_user_subscriptions_getter(get_user_subscriptions: GetUserSubscriptions, current_user: CurrentUserProxy, **_: Any) -> dict:
    """Get user subscriptions."""
    subs = await get_user_subscriptions(current_user.user)
    return {
        "subscriptions": subs,
    }
