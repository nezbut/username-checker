from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from username_checker.infrastructure.tkq.tasks import CALLBACK_SUB_ID_PREFIX

router = Router()


@router.callback_query(F.data.startswith(CALLBACK_SUB_ID_PREFIX))
async def username_available_ok(callback: CallbackQuery) -> None:
    """It is triggered when a notification arrives that the username is available."""
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.delete()
