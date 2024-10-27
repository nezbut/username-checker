from typing import Optional
from uuid import UUID

from username_checker.core.entities.user import User
from username_checker.core.entities.username import Username, UsernameStatus
from username_checker.core.interfaces import username as interfaces


async def check_username(username: Username, checker: interfaces.UsernameChecker) -> UsernameStatus:
    """
    Asynchronously checks the status of a username using a provided checker.

    :param username: The username to be checked.
    :param checker: The checker to use for checking the username.
    :return: The status of the username.
    """
    return await checker.check(username)


async def upsert_username(username: Username, upserter: interfaces.UsernameUpserter) -> Username:
    """
    Asynchronously upserts a username using the provided upserter.

    :param username: The username to be upserted.
    :type username: Username
    :param upserter: The upserter to perform the upsert operation.
    :type upserter: interfaces.UsernameUpserter
    :return: The upserted username.
    :rtype: Username
    """
    return await upserter.upsert(username)


async def delete_username(username_id: UUID, deleter: interfaces.UsernameDeleter) -> bool:
    """
    Deletes a username by its ID.

    :param username_id: The ID of the username to delete.
    :param deleter: The deleter to perform the deletion operation.
    :return: A boolean indicating whether the deletion was successful.
    """
    return await deleter.delete(username_id)


async def get_by_id(username_id: UUID, getter: interfaces.UsernameGetter) -> Optional[Username]:
    """
    Retrieves a username by its ID.

    :param username_id: The ID of the username to retrieve.
    :param getter: The getter to use for retrieving the username.
    :return: The retrieved username.
    """
    return await getter.get_by_id(username_id)


async def get_usernames(getter: interfaces.UsernameGetter, username_ids: Optional[list[UUID]] = None) -> list[Username]:
    """
    Retrieves a list of usernames using the provided getter.

    :param getter: The getter to use for retrieving the usernames.
    :type getter: interfaces.UsernameGetter
    :param username_ids: An optional list of username IDs to retrieve.
    :type username_ids: Optional[list[UUID]]
    :return: A list of retrieved usernames.
    :rtype: list[Username]
    """
    return await getter.get_usernames(username_ids)


async def get_by_value(value: str, getter: interfaces.UsernameGetter) -> Optional[Username]:
    """
    Retrieves a username by its value.

    :param value: The value of the username to retrieve.
    :param getter: The getter to use for retrieving the username.
    :return: The retrieved username.
    """
    return await getter.get_by_value(value)


async def get_used_usernames(user: User, getter: interfaces.UsernameGetter) -> list[Username]:
    """
    Retrieves all the user names that the user used.

    :param user: The user to check.
    :type user: User
    :param getter: The getter to use for retrieving the usernames.
    :type getter: interfaces.UsernameGetter
    :return: A list of all the user names that the user used.
    :rtype: list[Username]
    """
    return await getter.get_used_usernames(user)


async def get_available_usernames_for_user(user: User, getter: interfaces.UsernameGetter) -> list[Username]:
    """
    Gets all the usernames that are available to the user.

    :param user: The user.
    :type user: User
    :param getter: The getter to use for retrieving the usernames.
    :type getter: interfaces.UsernameGetter
    :return: A list of all the available usernames.
    :rtype: list[Username]
    """
    return await getter.get_available_usernames_for_user(user)


async def have_used(user: User, username: Username, inspector: interfaces.UsernameInspector) -> bool:
    """
    Checks if a user has used a username.

    :param user: The user to check.
    :type user: User
    :param username: The username
    :type username: Username
    :param inspector: The inspector to use for checking the username.
    :type inspector: interfaces.UsernameInspector
    :return: bool
    """
    return await inspector.have_used(user, username)
