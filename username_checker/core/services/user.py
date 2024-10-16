from typing import Optional

from username_checker.core.entities.user import User
from username_checker.core.interfaces import user as user_protocols


async def get_by_id(user_id: int, getter: user_protocols.UserGetter) -> Optional[User]:
    """
    Gets a user by their ID.

    :param user_id: The ID of the user to retrieve.
    :type user_id: int
    :return: The retrieved user.
    :rtype: User
    """
    return await getter.get_by_id(user_id)


async def get_users(getter: user_protocols.UserGetter, user_ids: Optional[list[int]] = None) -> list[User]:
    """
    Gets all users or users by their IDs.

    :param getter: The user getter.
    :type getter: user_protocols.UserGetter
    :param user_ids: An optional list of user IDs.
    :type user_ids: Optional[list[int]]
    :return: A list of all users or users by their IDs.
    :rtype: list[User]
    """
    return await getter.get_all(user_ids)


async def upsert_user(user: User, upserter: user_protocols.UserUpserter) -> User:
    """
    Upserts a user using the provided upserter.

    :param user: The user to be upserted.
    :type user: User
    :param upserter: The upserter to perform the upsert operation.
    :type upserter: user_protocols.UserUpserter
    :return: The upserted user.
    :rtype: User
    """
    return await upserter.upsert(user)


async def to_admins(user_ids: list[int], updater: user_protocols.UserUpdater) -> bool:
    """
    Changes a users to an admins.

    :param user_ids: The IDs of the users to change.
    :type user_ids: List[int]
    :return: True if the users was changed to an admin, False otherwise.
    :rtype: bool
    """
    return await updater.to_admins(user_ids)


async def to_superusers(user_ids: list[int], updater: user_protocols.UserUpdater) -> bool:
    """
    Changes a users to an superusers.

    :param user_ids: The IDs of the users to change.
    :type user_ids: List[int]
    :return: True if the users was changed to an superusers, False otherwise.
    :rtype: bool
    """
    return await updater.to_superusers(user_ids)
