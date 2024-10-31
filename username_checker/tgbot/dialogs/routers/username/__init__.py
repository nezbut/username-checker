from aiogram_dialog import Dialog

from username_checker.tgbot.dialogs.routers.username import windows

username_dialog = Dialog(
    *windows.get_windows(),
    name="username_dialog",
)

__all__ = ["username_dialog"]
