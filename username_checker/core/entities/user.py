from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LanguageLocale(Enum):

    """Enum representing the supported languages."""

    EN = "en"
    RU = "ru"


@dataclass
class User:

    """
    Represents a user in the system.

    :param id: The ID of the user.
    :param username: The username of the user.
    :param joined_us: The date and time when the user joined the system.
    :param last_activity: The date and time when the user last sent a message.
    :param language: The preferred language of the user.
    :param is_admin: Whether the user is an admin.
    :param is_superuser: Whether the user is a superuser.
    :param is_banned: Whether the user is banned.
    """

    id: int
    username: str
    joined_us: datetime
    last_activity: datetime
    language: LanguageLocale
    is_admin: bool
    is_superuser: bool
    is_banned: bool
