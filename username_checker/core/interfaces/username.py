from typing import Optional, Protocol
from uuid import UUID

from username_checker.core.entities.user import User
from username_checker.core.entities.username import Username, UsernameStatus


class UsernameChecker(Protocol):

    """A protocol for checking the username status."""

    async def check(self, username: Username) -> UsernameStatus:
        """
        Checking a username status.

        :param username: The username to be checked.
        :type username: Username
        :return: username status
        :rtype: UsernameStatus
        """
        ...


class UsernameInspector(Protocol):

    """A protocol for inspecting usernames."""

    async def have_used(self, user: User) -> bool:
        """
        Checks if a user has used a username.

        :param user: The user to check.
        :type user: User
        :return: bool
        """
        ...


class UsernameUpserter(Protocol):

    """A protocol for upserting usernames."""

    async def upsert(self, username: Username) -> Username:
        """
        Upserts a username.

        :param username: The username to be upserted.
        :type username: Username
        :return: The upserted username.
        """
        ...


class UsernameGetter(Protocol):

    """A protocol for getting usernames."""

    async def get_by_id(self, username_id: UUID) -> Optional[Username]:
        """
        Gets a username by its ID.

        :param username_id: The ID of the username to retrieve.
        :return: The retrieved username.
        """
        ...

    async def get_usernames(self, username_ids: Optional[list[UUID]] = None) -> list[Username]:
        """
        Gets all usernames or usernames by their IDs.

        :param username_ids: An optional list of username IDs.
        :return: A list of all usernames or usernames by their IDs.
        """
        ...

    async def get_by_value(self, value: str) -> Optional[Username]:
        """
        Gets a username by its value.

        :param value: The value of the username to retrieve.
        :return: The retrieved username.
        """
        ...

    async def get_used_usernames(self, user: User) -> list[Username]:
        """
        Returns all the user names that the user used.

        :param user: The user to check.
        :return: A list of all the user names that the user used.
        """
        ...

    async def get_available_usernames_for_user(self, user: User) -> list[Username]:
        """
        Gets all the usernames that are available to the user.

        :param user: The user.
        :type user: User
        :return: A list of all the available usernames.
        """
        ...


class UsernameDeleter(Protocol):

    """A protocol for deleting usernames."""

    async def delete(self, username_id: UUID) -> bool:
        """
        Deletes a username by its ID.

        :param username_id: The ID of the username to delete.
        :return: bool
        """
        ...
