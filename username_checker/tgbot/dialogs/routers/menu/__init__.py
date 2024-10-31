from aiogram_dialog import Dialog, LaunchMode

from username_checker.tgbot.dialogs.routers.menu import windows

menu_dialog = Dialog(
    *windows.get_windows(),
    launch_mode=LaunchMode.ROOT,
    name="menu_dialog",
)

__all__ = ["menu_dialog"]
