from aiogram import Dispatcher

from username_checker.tgbot.handlers import callbacks, commands, username


def setup(dp: Dispatcher) -> None:
    """Setup all handlers."""
    dp.include_routers(
        commands.router,
        callbacks.router,
        username.router,
    )
