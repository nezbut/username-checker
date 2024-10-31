from aiogram_dialog import Dialog

from username_checker.tgbot.dialogs.routers.menu import menu_dialog
from username_checker.tgbot.dialogs.routers.subscriptions import subscriptions_dialog
from username_checker.tgbot.dialogs.routers.username import username_dialog


def get_dialogs() -> list[Dialog]:
    """
    Returns a list of Dialog objects.

    :return: A list of Dialog objects.
    :rtype: list[Dialog]
    """
    return [
        menu_dialog,
        subscriptions_dialog,
        username_dialog,
    ]


__all__ = ["get_dialogs"]
