from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

commands_router = Router()


@commands_router.message(CommandStart())
async def start_command(message: Message) -> None:
    """Handle start command."""
    ...
