from adaptix import load
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from username_checker.core.entities.subscription import Interval
from username_checker.core.entities.username import Username
from username_checker.tgbot.dialogs.keys.username import UsernameDialogDataKeys
from username_checker.tgbot.dialogs.states.username import UsernameDialogStates
from username_checker.tgbot.utils.data import get_middleware_data


async def subscribe_username_on_click(callback: CallbackQuery, _: Select, manager: DialogManager, interval: Interval) -> None:
    """Subscribes to the username on click."""
    data = get_middleware_data(manager.middleware_data)
    username = load(
        manager.dialog_data[UsernameDialogDataKeys.USERNAME],
        Username,
    )
    subscribe = data["subscribe_check_username"]

    await subscribe(data["current_user"].user, username, interval)
    await manager.switch_to(UsernameDialogStates.MAIN)
