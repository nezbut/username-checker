from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Start

from username_checker.tgbot.dialogs.routers.menu.handlers import main as main_handlers
from username_checker.tgbot.dialogs.states.menu import MenuDialogStates
from username_checker.tgbot.dialogs.states.subscriptions import SubscriptionsDialogStates
from username_checker.tgbot.dialogs.widgets.i18n import I18NWidget

main_window = Window(
    I18NWidget("main-menu-text-menu-dialog"),
    Start(
        I18NWidget("my-subs-button-menu-dialog"),
        id="subs_dialog_start",
        state=SubscriptionsDialogStates.MAIN,
    ),
    Button(
        I18NWidget("upload-json-file-button-menu-dialog"),
        id="upload_json_file",
        on_click=main_handlers.upload_json_file_on_click,
    ),
    state=MenuDialogStates.MAIN,
)
