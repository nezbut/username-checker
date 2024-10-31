from pathlib import Path
from typing import Protocol

from username_checker.core.entities.username import Username


class UsernameUploader(Protocol):

    """A protocol for uploading usernames."""

    async def upload(self, usernames: list[Username]) -> Path:
        """
        Uploads a list of usernames.

        :param usernames: A list of usernames to upload.
        :type usernames: list[Username]
        :return: path to uploaded
        :rtype: Path
        """
        ...
