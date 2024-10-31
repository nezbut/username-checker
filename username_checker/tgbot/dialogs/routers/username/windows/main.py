from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Row, Start, SwitchTo
from aiogram_dialog.widgets.text import Format

from username_checker.tgbot.dialogs.routers.username.getters.main import main_window_getter
from username_checker.tgbot.dialogs.routers.username.handlers import main as handlers
from username_checker.tgbot.dialogs.states.menu import MenuDialogStates
from username_checker.tgbot.dialogs.states.username import UsernameDialogStates
from username_checker.tgbot.dialogs.widgets.i18n import I18NWidget

main_window = Window(
    I18NWidget("username-info-text-username-dialog"),
    Format("<a href='https://fragment.com/username/{value}'>Fragment</a>"),
    Row(
        Button(
            I18NWidget("check-username-button-username-dialog"),
            id="check_username",
            on_click=handlers.check_username_on_click,
        ),
        SwitchTo(
            I18NWidget("subscribe-username-button-username-dialog"),
            id="interval_sel_switch",
            state=UsernameDialogStates.INTERVAL_SELECTION,
            when=~F["is_subscribed"],
        ),
        Button(
            I18NWidget("unsubscribe-username-button-username-dialog"),
            id="unsubscribe_username",
            on_click=handlers.unsubscribe_username_on_click,
            when=F["is_subscribed"],
        ),
    ),
    Start(
        I18NWidget("main-menu-button"),
        id="menu_dialog_start",
        state=MenuDialogStates.MAIN,
    ),
    state=UsernameDialogStates.MAIN,
    getter=main_window_getter,
)
