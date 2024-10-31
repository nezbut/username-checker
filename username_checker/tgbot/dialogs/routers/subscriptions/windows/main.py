from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from username_checker.tgbot.dialogs.routers.subscriptions.getters.main import get_user_subscriptions_getter
from username_checker.tgbot.dialogs.routers.subscriptions.handlers.main import switch_to_subscription_profile_on_click
from username_checker.tgbot.dialogs.states.subscriptions import SubscriptionsDialogStates
from username_checker.tgbot.dialogs.widgets.i18n import I18NWidget

main_window = Window(
    I18NWidget("my-subs-text-subscriptions-dialog"),
    ScrollingGroup(
        Select(
            Format("{item.username.value}"),
            id="subs_select",
            item_id_getter=lambda item: str(item.id),
            items="subscriptions",
            on_click=switch_to_subscription_profile_on_click,
        ),
        id="subs_scroll",
        width=3,
        height=5,
    ),
    Cancel(
        I18NWidget("back-button"),
    ),
    state=SubscriptionsDialogStates.MAIN,
    getter=get_user_subscriptions_getter,
)
