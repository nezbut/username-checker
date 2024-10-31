from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Select, SwitchTo
from aiogram_dialog.widgets.text import Format

from username_checker.core.entities.subscription import Interval
from username_checker.tgbot.dialogs.routers.username.getters.interval_selection import interval_buttons_getter
from username_checker.tgbot.dialogs.routers.username.handlers import interval_selection as handlers
from username_checker.tgbot.dialogs.states.username import UsernameDialogStates
from username_checker.tgbot.dialogs.widgets.i18n import I18NWidget

interval_selection_window = Window(
    I18NWidget("interval-selection-text-username-dialog"),
    Group(
        Select(
            Format("{item[interval_readable]}"),
            id="interval_btn_sel",
            item_id_getter=lambda item: item["interval_seconds"],
            items="interval_buttons",
            on_click=handlers.subscribe_username_on_click,
            type_factory=lambda data: Interval(int(data)),
        ),
        width=3,
    ),
    SwitchTo(
        I18NWidget("cancel-button"),
        id="interval_sel_cancel",
        state=UsernameDialogStates.MAIN,
    ),
    state=UsernameDialogStates.INTERVAL_SELECTION,
    getter=interval_buttons_getter,
)
