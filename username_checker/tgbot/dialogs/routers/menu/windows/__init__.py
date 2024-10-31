from aiogram_dialog import Window

from username_checker.tgbot.dialogs.routers.menu.windows.main import main_window


def get_windows() -> list[Window]:
    """
    Returns a list of Window objects.

    :return: A list of Window objects.
    :rtype: list[Window]
    """
    return [
        main_window,
    ]


__all__ = ["get_windows"]
