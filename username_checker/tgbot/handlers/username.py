from adaptix import dump
from aiogram import F, Router
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import StartMode
from fluentogram import TranslatorRunner

from username_checker.core.interactors.username import GetUsername
from username_checker.infrastructure.proxy.user import CurrentUserProxy
from username_checker.tgbot.dialogs.keys.username import UsernameDialogStartDataKeys
from username_checker.tgbot.dialogs.states.username import UsernameDialogStates
from username_checker.tgbot.filters.username import MAX_USERNAME_LENGTH, MIN_USERNAME_LENGTH, UsernameFilter

router = Router()


@router.message(UsernameFilter())
async def username_handler(
    message: Message,
    username_value: str,
    get_username: GetUsername,
    dialog_manager: DialogManager,
    current_user: CurrentUserProxy,
) -> None:
    """Handle username."""
    username = await get_username(username_value, current_user.user)
    await dialog_manager.start(
        state=UsernameDialogStates.MAIN,
        data={UsernameDialogStartDataKeys.USERNAME: dump(username)},
        mode=StartMode.RESET_STACK,
    )


@router.message(F.text)
async def text_not_username_handler(message: Message, i18n: TranslatorRunner) -> None:
    """Handle text not username."""
    text = i18n.get(
        "text-not-username-username-handlers",
        min_length=MIN_USERNAME_LENGTH,
        max_length=MAX_USERNAME_LENGTH,
    )
    await message.answer(text)
