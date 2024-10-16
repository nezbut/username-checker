from aiogram import Dispatcher
from dishka import AsyncContainer
from structlog.stdlib import BoundLogger

from username_checker.common.settings import Settings
from username_checker.core.services.user import to_superusers
from username_checker.infrastructure.database.rdb.holder import HolderDAO
from username_checker.tgbot import handlers, middlewares


def setup_dispatcher(dp: Dispatcher, settings: Settings, logger: BoundLogger) -> Dispatcher:
    """Setup all in dispatcher."""
    handlers.setup(dp)
    middlewares.setup(
        dp=dp,
        settings=settings,
        logger=logger,
    )
    return dp


async def init(container: AsyncContainer, settings: Settings, logger: BoundLogger) -> None:
    """Init function."""
    async with container() as req:
        holder: HolderDAO = await req.get(HolderDAO)
        await to_superusers(settings.bot.admin.superusers, holder.user)
        await logger.ainfo("Set superusers: %s", settings.bot.admin.superusers)
        await holder.commit()
