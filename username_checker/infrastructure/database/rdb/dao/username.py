from typing import Optional
from uuid import UUID

from adaptix import dump
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from username_checker.core.entities.user import User
from username_checker.core.entities.username import Username, UsernameStatus
from username_checker.infrastructure.database.rdb.dao.base import BaseDAO
from username_checker.infrastructure.database.rdb.models import UsernameORM, UserORM


class UsernameDAO(BaseDAO[UsernameORM]):

    """A class representing the DAO for the Username model."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(UsernameORM, session)

    async def have_used(self, user: User, username: Username) -> bool:
        """
        Checks if a user has used a username.

        :param user: The user to check.
        :type user: User
        :param username: The username
        :type username: Username
        :return: bool
        """
        stmt = (
            select(self._model)
            .where(
                self._model.id == username.id,
                self._model.used_usernames_by.any(UserORM.id == user.id),
            )
        )
        result = await self.session.execute(stmt)
        return bool(result.scalars().all())

    async def get_by_id(self, username_id: UUID) -> Optional[Username]:
        """
        Retrieves a Username by their ID.

        :param user_id: The ID of the Username to retrieve.
        :type username_id: UUID

        :return: The Username entity.
        :rtype: Username
        """
        username = await self._get_by_id(username_id)
        return username.to_entity() if username else None

    async def get_usernames(self, username_ids: Optional[list[UUID]] = None) -> list[Username]:
        """
        Gets all usernames or usernames by their IDs.

        :param username_ids: An optional list of username IDs.
        :return: A list of all usernames or usernames by their IDs.
        """
        if not username_ids:
            usernames = await self._get_all()
        else:
            stmt = (
                select(self._model)
                .where(self._model.id.in_(username_ids))
            )
            usernames = (await self.session.scalars(stmt)).all()
        return [username.to_entity() for username in usernames]

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
        stmt = (
            select(self._model)
            .where(self._model.used_usernames_by.any(UserORM.id == user.id))
        )
        result = await self.session.scalars(stmt)
        usernames = result.all()
        return [username.to_entity() for username in usernames]

    async def get_available_usernames_for_user(self, user: User) -> list[Username]:
        """
        Gets all the usernames that are available to the user.

        :param user: The user.
        :type user: User
        :return: A list of all the available usernames.
        """
        stmt = (
            select(self._model)
            .where(
                self._model.status == UsernameStatus.AVAILABLE,
                self._model.used_usernames_by.notany(UserORM.id == user.id),
            )
        )
        result = await self.session.scalars(stmt)
        usernames = result.all()
        return [username.to_entity() for username in usernames]

    async def upsert(self, username: Username) -> Username:
        """
        Upserts a Username into the database.

        :param Username: The Username to be upserted.
        :type Username: Username

        :return: The upserted Username.
        :rtype: Username
        """
        kwargs = dump(username)
        kwargs["status"] = username.status

        saved_username = await self.session.execute(
            insert(self._model)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(
                    self._model.id,), set_=kwargs, where=self._model.id == username.id,
            )
            .returning(self._model),
        )
        return saved_username.scalar_one().to_entity()

    async def delete(self, username_id: UUID) -> bool:
        """
        Deletes a username by its ID.

        :param username_id: The ID of the username to delete.
        :return: bool
        """
        stmt = delete(self._model).where(self._model.id == username_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
