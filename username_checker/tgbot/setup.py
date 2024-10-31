from aiogram import Dispatcher
from dishka import AsyncContainer
from structlog.stdlib import BoundLogger

from username_checker.common.settings import Settings
from username_checker.infrastructure.proxy.user import UserProxy
from username_checker.tgbot import dialogs, handlers, middlewares


def setup_dispatcher(dp: Dispatcher, settings: Settings, logger: BoundLogger) -> Dispatcher:
    """Setup all in dispatcher."""
    handlers.setup(dp)
    bg_manager_factory = dialogs.setup(dp)
    middlewares.setup(
        dp=dp,
        bg_manager_factory=bg_manager_factory,
        settings=settings,
        logger=logger,
    )
    return dp


async def init(container: AsyncContainer, settings: Settings, logger: BoundLogger) -> None:
    """Init function."""
    async with container() as req:
        user_proxy: UserProxy = await req.get(UserProxy)
        await user_proxy.to_superusers(settings.bot.admin.superusers, commit=True)
        await logger.ainfo("Set superusers: %s", settings.bot.admin.superusers)
