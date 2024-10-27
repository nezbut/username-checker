from aiogram import Dispatcher
from aiogram_dialog.api.protocols import BgManagerFactory
from structlog.stdlib import BoundLogger

from username_checker.common.settings import Settings
from username_checker.tgbot.middlewares.i18n import I18NMiddleware
from username_checker.tgbot.middlewares.init import InitMiddleware
from username_checker.tgbot.middlewares.interactors import InteractorsMiddleware
from username_checker.tgbot.middlewares.logs import LoggingMiddleware
from username_checker.tgbot.middlewares.throttling import ThrottlingMiddleware
from username_checker.tgbot.middlewares.user import BannedUserMiddleware, TrackUserMiddleware


def setup(
    dp: Dispatcher,
    bg_manager_factory: BgManagerFactory,
    settings: Settings,
    logger: BoundLogger,
) -> None:
    """Setup middlewares."""
    dp.update.outer_middleware(
        InitMiddleware(
            bg_manager_factory=bg_manager_factory,
            settings=settings,
        ),
    )
    dp.update.outer_middleware(I18NMiddleware())
    dp.update.outer_middleware(
        LoggingMiddleware(
            logger=logger,
        ),
    )
    dp.update.outer_middleware(TrackUserMiddleware())
    banned = BannedUserMiddleware()
    dp.callback_query.middleware(banned)
    dp.message.middleware(banned)
    dp.message.middleware(
        ThrottlingMiddleware(
            limit=settings.bot.throttling_rate_limit,
        ),
    )
    dp.update.middleware(InteractorsMiddleware())
