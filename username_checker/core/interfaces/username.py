from typing import Protocol


class UsernameChecker(Protocol):

    """A protocol for checking the validity of usernames."""

    async def check(self, username: str) -> bool:
        """
        Checks if a given username is valid.

        :param username: The username to be checked.
        :return: True if the username is valid, False otherwise.
        """
        ...
