from typing import Any
from uuid import UUID

from adaptix import dump
from aiogram_dialog import DialogManager

from username_checker.core.interfaces.subscription import SubscriptionGetter
from username_checker.core.services.subscription import get_by_id as get_sub_by_id
from username_checker.tgbot.dialogs.keys.subscriptions import SubscriptionsDialogDataKeys


async def get_current_subscription_getter(dialog_manager: DialogManager, sub_getter_i: SubscriptionGetter, **_: Any) -> Any:
    """Get current subscription."""
    sub_id: str = dialog_manager.dialog_data[SubscriptionsDialogDataKeys.CURRENT_SUBSCRIPTION_ID]
    sub = await get_sub_by_id(UUID(sub_id), sub_getter_i)
    if sub:
        data = {
            "interval": sub.interval.value,
            **dump(sub.username),
            **dump(sub.subscriber),
        }
        data["id"] = sub.id
        data["username_id"] = sub.username.id
        data["subscriber_id"] = sub.subscriber.id
        return data
    return None
