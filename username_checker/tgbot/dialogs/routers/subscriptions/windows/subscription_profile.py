from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo

from username_checker.tgbot.dialogs.routers.subscriptions.getters.subscription_profile import get_current_subscription_getter
from username_checker.tgbot.dialogs.routers.subscriptions.handlers.subscription_profile import unsubscribe_username_on_click
from username_checker.tgbot.dialogs.states.subscriptions import SubscriptionsDialogStates
from username_checker.tgbot.dialogs.widgets.i18n import I18NWidget

subscription_profile_window = Window(
    I18NWidget("subscription-profile-text-subscriptions-dialog"),
    SwitchTo(
        I18NWidget("unsubscribe-username-button-subscriptions-dialog"),
        id="unsubscribe_username",
        state=SubscriptionsDialogStates.MAIN,
        on_click=unsubscribe_username_on_click,
    ),
    SwitchTo(
        I18NWidget("back-button"),
        id="back_sub_profile",
        state=SubscriptionsDialogStates.MAIN,
    ),
    state=SubscriptionsDialogStates.SUBSCRIPTION_PROFILE,
    getter=get_current_subscription_getter,
)
