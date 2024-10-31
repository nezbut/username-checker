from uuid import UUID

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from username_checker.tgbot.dialogs.keys.subscriptions import SubscriptionsDialogDataKeys
from username_checker.tgbot.utils.data import get_middleware_data


async def unsubscribe_username_on_click(callback: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """Unsubscribes from the subscription."""
    data = get_middleware_data(manager.middleware_data)
    unsubscribe = data["unsubscribe_check_username"]
    sub_id = UUID(
        manager.dialog_data.pop(
            SubscriptionsDialogDataKeys.CURRENT_SUBSCRIPTION_ID,
        ),
    )

    await unsubscribe(sub_id)
