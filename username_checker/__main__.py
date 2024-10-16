import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher

from username_checker.common.log.configuration import LoggerName
from username_checker.common.log.installer import LoggersInstaller
from username_checker.common.settings import Settings
from username_checker.infrastructure.tkq.constants import taskiq_broker
from username_checker.tgbot.di.factory import create_container
from username_checker.tgbot.setup import init, setup_dispatcher


async def start_polling(settings: Settings) -> None:
    """Start polling for telegram bot"""
    container = create_container(settings)
    installer: LoggersInstaller = await container.get(LoggersInstaller)
    bot: Bot = await container.get(Bot)
    dp_not_setup: Dispatcher = await container.get(Dispatcher)
    bot_info = await bot.get_me()
    logger = installer.get_logger(
        LoggerName.BOT, bot_name=bot_info.full_name, id=bot_info.id,
    )
    dp = setup_dispatcher(dp_not_setup, settings, logger)

    try:
        await init(container, settings, logger)
        await bot.delete_webhook(drop_pending_updates=True)
        await taskiq_broker.startup()
        await logger.ainfo("Start polling for telegram bot")
        await dp.start_polling(bot)
    finally:
        await taskiq_broker.shutdown()
        await logger.ainfo("Close bot session")
        await bot.session.close()
        await logger.ainfo("Stop polling")
        with suppress(RuntimeError):
            await dp.stop_polling()


if __name__ == "__main__":
    _settings = Settings.from_dynaconf()
    asyncio.run(start_polling(_settings))
