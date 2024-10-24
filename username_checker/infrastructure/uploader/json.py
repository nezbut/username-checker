import json
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Optional, Union

import aiofiles
from adaptix import dump

from username_checker.core.entities.username import Username
from username_checker.core.interfaces.uploader import UsernameUploader

FileNameGenerator = Callable[[], str]


class JSONFileUsernameUploader(UsernameUploader):

    """A class responsible for uploading usernames in JSON file."""

    def __init__(self, path: Optional[Union[str, Path]] = None, file_name_generator: Optional[FileNameGenerator] = None) -> None:
        self._path = Path(path) if path else Path(__file__) / "usernames"
        self._file_name_generator = file_name_generator or self._default_file_name_generator()

    async def upload(self, usernames: list[Username]) -> str:
        """
        Uploads a list of usernames.

        :param usernames: A list of usernames to upload.
        :type usernames: list[Username]
        :return: path to uploaded
        :rtype: str
        """
        file_name = self._file_name_generator()
        path = str(self._path / file_name)
        usernames_data = [dump(username) for username in usernames]
        usernames_json = json.dumps(usernames_data)
        async with aiofiles.open(path, "w") as file:
            await file.write(usernames_json)
        return path

    def _default_file_name_generator(self) -> FileNameGenerator:
        return lambda: f"usernames_{datetime.now(UTC).strftime("%d.%m.%Y_%H_%M_%S")}.json"
