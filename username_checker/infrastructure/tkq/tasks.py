from typing import Annotated

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dishka.integrations.taskiq import FromDishka as Depends
from dishka.integrations.taskiq import inject
from fluentogram import TranslatorHub
from taskiq import Context, TaskiqDepends

from username_checker.core.entities.subscription import Subscription
from username_checker.core.entities.username import UsernameStatus
from username_checker.core.interactors.username import CheckUsername
from username_checker.core.interfaces.commiter import Commiter
from username_checker.core.interfaces.subscription import SubscriptionDeleter
from username_checker.core.services.subscription import delete_subscription
from username_checker.infrastructure.proxy.user import UserProxy
from username_checker.infrastructure.tkq.constants import schedule_source, taskiq_broker

ContextAnn = Annotated[Context, TaskiqDepends()]
CALLBACK_SUB_ID_PREFIX = "sub_id_"


@taskiq_broker.task()
@inject
async def check_username_task(
    subscription: Subscription,
    bot: Depends[Bot],
    check: Depends[CheckUsername],
    hub: Depends[TranslatorHub],
    proxy: Depends[UserProxy],
    commiter: Depends[Commiter],
    sub_deleter: Depends[SubscriptionDeleter],
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
    if username.status == UsernameStatus.AVAILABLE:
        schedule_id: str = context.message.labels["schedule_id"]
        button = InlineKeyboardButton(
            text=i18n.get("ok-button"),
            callback_data=f"{CALLBACK_SUB_ID_PREFIX}{subscription.id}",
        )
        markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
        text = i18n.get(
            "username-is-available-check-username",
            username=username.value,
        )
        await bot.send_message(chat_id=user.id, text=text, reply_markup=markup)
        await delete_subscription(subscription.id, sub_deleter)
        await schedule_source.delete_schedule(schedule_id=schedule_id)
        await commiter.commit()
