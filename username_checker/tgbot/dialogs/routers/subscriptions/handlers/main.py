from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from username_checker.tgbot.dialogs.keys.subscriptions import SubscriptionsDialogDataKeys
from username_checker.tgbot.dialogs.states.subscriptions import SubscriptionsDialogStates


async def switch_to_subscription_profile_on_click(callback: CallbackQuery, _: Select, manager: DialogManager, sub_id: str) -> None:
    """Switches to the subscription profile."""
    manager.dialog_data[SubscriptionsDialogDataKeys.CURRENT_SUBSCRIPTION_ID] = sub_id
    await manager.switch_to(SubscriptionsDialogStates.SUBSCRIPTION_PROFILE)
