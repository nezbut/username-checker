from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import ShowMode

from username_checker.tgbot.dialogs.states.menu import MenuDialogStates

router = Router()


@router.message(CommandStart())
async def start_command(_: Message, dialog_manager: DialogManager) -> None:
    """Handle start command."""
    await dialog_manager.start(
        MenuDialogStates.MAIN,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
