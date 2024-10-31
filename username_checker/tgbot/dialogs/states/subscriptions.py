from aiogram.fsm.state import State, StatesGroup


class SubscriptionsDialogStates(StatesGroup):

    """States for the subscriptions dialog."""

    MAIN = State()
    SUBSCRIPTION_PROFILE = State()
