from typing import Optional, Protocol

from username_checker.core.entities.user import User


class UserUpserter(Protocol):

    """A protocol for upserting products."""

    async def upsert(self, user: User) -> User:
        """
        Upserts a product.

        :param product: The product to be upserted.
        :type product: Product
        :return: The upserted product.
        :rtype: Product
        """
        ...


class UserGetter(Protocol):

    """A protocol for getting users."""

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Gets a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :type user_id: int
        :return: The retrieved user.
        :rtype: User
        """
        ...

    async def get_all(self, ids: Optional[list[int]] = None) -> list[User]:
        """
        Gets all users or users by their IDs.

        :return: A list of all users or users by their IDs.
        :rtype: list[User]
        """
        ...


class UserUpdater(Protocol):

    """A protocol for updating users."""

    async def to_admins(self, user_ids: list[int]) -> bool:
        """
        Changes a users to an admins.

        :param user_ids: The IDs of the users to change.
        :type user_ids: List[int]
        :return: True if the users was changed to an admin, False otherwise.
        :rtype: bool
        """
        ...

    async def to_superusers(self, user_ids: list[int]) -> bool:
        """
        Changes a users to an superusers.

        :param user_ids: The IDs of the users to change.
        :type user_ids: List[int]
        :return: True if the users was changed to an superusers, False otherwise.
        :rtype: bool
        """
        ...
