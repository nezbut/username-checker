from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from username_checker.tgbot.utils.data import get_middleware_data


async def upload_json_file_on_click(callback: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """Handles the event when the Upload JSON file button is clicked."""
    data = get_middleware_data(manager.middleware_data)
    upload = data["upload_available_usernames"]
    current_user = data["current_user"]
    path = await upload(current_user.user)
    file = FSInputFile(path)
    if isinstance(callback.message, Message):
        await callback.message.answer_document(file)
    path.unlink()
