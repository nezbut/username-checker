from aiogram.fsm.state import State, StatesGroup


class UsernameDialogStates(StatesGroup):

    """States for the username dialog."""

    MAIN = State()
    INTERVAL_SELECTION = State()
