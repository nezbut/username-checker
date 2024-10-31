from aiogram_dialog import Dialog

from username_checker.tgbot.dialogs.routers.subscriptions import windows

subscriptions_dialog = Dialog(
    *windows.get_windows(),
    name="subscriptions_dialog",
)

__all__ = ["subscriptions_dialog"]
