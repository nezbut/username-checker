from datetime import UTC, datetime
from typing import Any, Optional

from adaptix import dump, load

from username_checker.core.entities.user import LanguageLocale, User
from username_checker.core.interfaces.commiter import Commiter
from username_checker.core.services import user as user_service
from username_checker.infrastructure.clients.cache.base import BaseCacheClient
from username_checker.infrastructure.clients.cache.key import UserCacheKey
from username_checker.infrastructure.database.rdb.dao.user import UserDAO


class UserProxy:

    """A class representing a proxy for user."""

    def __init__(self, dao: UserDAO, cache: BaseCacheClient, commiter: Commiter):
        self._dao = dao
        self._cache = cache
        self._commiter = commiter

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Gets a user by its ID.

        :param user_id: The ID of the user to retrieve.
        :type user_id: int
        :return: The retrieved user.
        :rtype: User
        """
        cache_key = UserCacheKey(user_id=user_id)
        user_from_cache: Optional[dict[str, Any]] = await self._cache.get(cache_key)

        if user_from_cache is not None:
            return load(user_from_cache, User)

        return await user_service.get_by_id(user_id, self._dao)

    async def get_all(self, ids: Optional[list[int]] = None) -> list[User]:
        """
        Gets all users or users by their IDs.

        :return: A list of all users or users by their IDs.
        :rtype: list[User]
        """
        return await user_service.get_users(self._dao, user_ids=ids)

    async def upsert(self, user: User, *, commit: bool = False) -> User:
        """
        Upserts the user data into the cache and the database.

        :param user: The user data to upsert.
        :type user: User
        :return: The upserted user.
        :rtype: User
        """
        cache_key = UserCacheKey(user_id=user.id)
        upserted_user = await user_service.upsert_user(user, self._dao)
        upserted_user_data = dump(upserted_user)
        await self._cache.set(cache_key, upserted_user_data)
        if commit:
            await self._commiter.commit()
        return upserted_user

    async def ban(self, user: User, *, commit: bool = False) -> User:
        """
        Bans the user.

        :param user: The user to ban.
        :type user: User
        :param commit: Whether to commit the changes to the database.
        :type commit: bool
        :return: The banned user.
        :rtype: User
        """
        user.is_banned = True
        return await self.upsert(user, commit=commit)

    async def un_ban(self, user: User, *, commit: bool = False) -> User:
        """
        Un-bans the user.

        :param user: The user to un-ban.
        :type user: User
        :param commit: Whether to commit the changes to the database.
        :type commit: bool
        :return: The unbanned user.
        :rtype: User
        """
        user.is_banned = False
        return await self.upsert(user, commit=commit)

    async def to_casual(self, user: User, *, commit: bool = False) -> User:
        """
        Changes a users to a casual users.

        :param user: The user to change.
        :type user: User
        :param commit: Whether to commit the changes to the database.
        :type commit: bool
        :return: The changed user.
        :rtype: User
        """
        user.is_admin = False
        user.is_superuser = False
        return await self.upsert(user, commit=commit)

    async def to_admins(self, user_ids: list[int], *, commit: bool = False) -> bool:
        """
        Changes a users to an admins.

        :param user_ids: The IDs of the users to change.
        :type user_ids: List[int]
        :param commit: Whether to commit the changes to the database.
        :type commit: bool
        :return: True if the users was changed to an admin, False otherwise.
        :rtype: bool
        """
        cache_keys = [UserCacheKey(user_id=user_id) for user_id in user_ids]
        for cache_key in cache_keys:
            await self._cache.delete(cache_key)
        result = await user_service.to_admins(user_ids, self._dao)
        if commit:
            await self._commiter.commit()
        return result

    async def to_superusers(self, user_ids: list[int], *, commit: bool = False) -> bool:
        """
        Changes a users to a superusers.

        :param user_ids: The IDs of the users to change.
        :type user_ids: List[int]
        :param commit: Whether to commit the changes to the database.
        :type commit: bool
        :return: True if the users was changed to an superusers, False otherwise.
        :rtype: bool
        """
        cache_keys = [UserCacheKey(user_id=user_id) for user_id in user_ids]
        for cache_key in cache_keys:
            await self._cache.delete(cache_key)
        result = await user_service.to_superusers(user_ids, self._dao)
        if commit:
            await self._commiter.commit()
        return result


class CurrentUserProxy:

    """
    A class representing the current user proxy.

    This class provides methods to interact with the current user.
    """

    def __init__(self, user: User, user_proxy: UserProxy):
        self._user = user
        self._user_proxy = user_proxy

    @property
    def user(self) -> User:
        """
        Current user.

        :return: The user.
        :rtype: User
        """
        return self._copy_user()

    def _copy_user(self) -> User:
        return self._user

    async def change_language(self, new_language: LanguageLocale, *, commit: bool = False) -> User:
        """
        Changes the language of the current user to the specified `new_language`.

        :param new_language: The new preferred language of the user.
        :type new_language: LanguageLocale
        :param commit: Whether to commit the changes to the database.
        :type commit: bool
        :return: The updated user with the new language.
        :rtype: User
        """
        self._user.language = new_language
        return await self._user_proxy.upsert(self._user, commit=commit)

    async def change_username(self, new_username: str, *, commit: bool = False) -> User:
        """
        Changes the username of the current user to the specified `new_username`.

        :param new_username: The new username of the user.
        :type new_username: str
        :param commit: Whether to commit the changes to the database.
        :type commit: bool
        :return: The updated user with the new username.
        :rtype: User
        """
        self._user.username = new_username
        return await self._user_proxy.upsert(self._user, commit=commit)

    async def update_last_activity(self, *, commit: bool = False) -> User:
        """
        Updates the last activity timestamp of the current user.

        :param commit: Whether to commit the changes to the database.
        :type commit: bool
        :return: The updated user with the new last activity timestamp.
        :rtype: User
        """
        self._user.last_activity = datetime.now(UTC)
        return await self._user_proxy.upsert(self._user, commit=commit)
