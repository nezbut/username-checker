from typing import Any

from adaptix import load
from aiogram_dialog import DialogManager

from username_checker.core.entities.username import Username
from username_checker.core.interfaces.subscription import SubscriptionGetter
from username_checker.core.services.subscription import get_by_subscriber_and_username
from username_checker.infrastructure.proxy.user import CurrentUserProxy
from username_checker.tgbot.dialogs.keys.username import UsernameDialogDataKeys, UsernameDialogStartDataKeys


async def main_window_getter(
        dialog_manager: DialogManager,
        current_user: CurrentUserProxy,
        sub_getter_i: SubscriptionGetter,
        **_: Any,
) -> Any:
    """Get username"""
    username_from_data = dialog_manager.dialog_data.get(
        UsernameDialogDataKeys.USERNAME,
    )
    if username_from_data is not None:
        username = username_from_data
    elif isinstance(dialog_manager.start_data, dict):
        username = dialog_manager.start_data[UsernameDialogStartDataKeys.USERNAME]
        dialog_manager.dialog_data[UsernameDialogDataKeys.USERNAME] = username
    else:
        raise ValueError("Username not found")
    sub = await get_by_subscriber_and_username(current_user.user, load(username, Username), sub_getter_i)
    return {
        **username,
        "is_subscribed": bool(sub),
    }
