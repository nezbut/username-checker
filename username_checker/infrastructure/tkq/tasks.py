from typing import Annotated

from aiogram import Bot
from dishka.integrations.taskiq import FromDishka as Depends
from dishka.integrations.taskiq import inject
from fluentogram import TranslatorHub
from taskiq import Context, TaskiqDepends

from username_checker.core.entities.subscription import Subscription
from username_checker.core.entities.username import UsernameStatus
from username_checker.core.interactors.username import CheckUsername
from username_checker.infrastructure.proxy.user import UserProxy
from username_checker.infrastructure.tkq.constants import schedule_source, taskiq_broker

ContextAnn = Annotated[Context, TaskiqDepends()]


@taskiq_broker.task()
@inject
async def check_username_task(
    subscription: Subscription,
    bot: Depends[Bot],
    check: Depends[CheckUsername],
    hub: Depends[TranslatorHub],
    proxy: Depends[UserProxy],
    context: ContextAnn,
) -> None:
    """
    A function that checks the availability of a username for a given subscription.

    :return: None
    """
    user = await proxy.get_by_id(subscription.subscriber.id)
    if user is None or user.is_banned:
        return
    i18n = hub.get_translator_by_locale(locale=user.language.value)
    username = await check(subscription.username)
    if username.status is UsernameStatus.AVAILABLE:
        schedule_id: str = context.message.labels["schedule_id"]
        text = i18n.get(
            "username-is-available-check-username",
            username=username.value,
        )
        await bot.send_message(chat_id=user.id, text=text)
        await schedule_source.delete_schedule(schedule_id=schedule_id)
