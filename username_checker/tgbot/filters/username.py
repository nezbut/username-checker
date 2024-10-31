from string import ascii_letters, digits
from typing import Any, Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

MIN_USERNAME_LENGTH = 5
MAX_USERNAME_LENGTH = 32


class UsernameFilter(BaseFilter):

    """A filter class that checks if a message text is a valid username."""

    def __init__(self) -> None:
        self._allowed = ascii_letters + digits + "_"

    async def __call__(self, message: Message) -> Union[dict[str, Any], bool]:
        """Checks if a message text is a valid username."""
        value = message.text
        if value is None:
            return False
        value = value[1:] if value.startswith("@") else value
        if (value.startswith("_") or value.endswith("_")) or not (MIN_USERNAME_LENGTH <= len(value) <= MAX_USERNAME_LENGTH):
            return False
        if value.isnumeric() or value[0].isnumeric():
            return False
        for char in value:
            if char not in self._allowed:
                return False
        return {"username_value": value.lower().strip()}
