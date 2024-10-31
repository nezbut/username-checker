from adaptix import dump, load
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from username_checker.core.entities.username import Username
from username_checker.core.services.subscription import get_by_subscriber_and_username
from username_checker.tgbot.dialogs.keys.username import UsernameDialogDataKeys
from username_checker.tgbot.utils.data import get_middleware_data


async def check_username_on_click(callback: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """Checks the username on click."""
    data = get_middleware_data(manager.middleware_data)
    username = load(
        manager.dialog_data[UsernameDialogDataKeys.USERNAME],
        Username,
    )
    check = data["check_username"]

    checked_username = await check(username)
    manager.dialog_data[UsernameDialogDataKeys.USERNAME] = dump(
        checked_username,
    )


async def unsubscribe_username_on_click(callback: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """Unsubscribes to the username on click."""
    data = get_middleware_data(manager.middleware_data)
    unsubscribe = data["unsubscribe_check_username"]
    username = load(
        manager.dialog_data[UsernameDialogDataKeys.USERNAME],
        Username,
    )

    sub = await get_by_subscriber_and_username(data["current_user"].user, username, data["sub_getter_i"])
    if sub is None:
        await data["logger"].aerror("Subscription not found")
        return

    await unsubscribe(sub.id)
