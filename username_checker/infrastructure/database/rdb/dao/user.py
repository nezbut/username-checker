from typing import Optional

from adaptix import dump
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from username_checker.core.entities.user import User
from username_checker.infrastructure.database.rdb.dao.base import BaseDAO
from username_checker.infrastructure.database.rdb.models import UserORM


class UserDAO(BaseDAO[UserORM]):

    """A class representing the DAO for the User model."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(UserORM, session)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :type user_id: int

        :return: The user entity.
        :rtype: User
        """
        user = await self._get_by_id(user_id)
        return user.to_entity() if user else None

    async def upsert(self, user: User) -> User:
        """
        Upserts a user into the database.

        :param user: The user to be upserted.
        :type user: User

        :return: The upserted user.
        :rtype: User
        """
        kwargs = dump(user)
        kwargs["joined_us"] = user.joined_us
        kwargs["last_activity"] = user.last_activity
        kwargs["language"] = user.language

        saved_user = await self.session.execute(
            insert(self._model)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(
                    self._model.id,), set_=kwargs, where=self._model.id == user.id,
            )
            .returning(self._model),
        )
        return saved_user.scalar_one().to_entity()

    async def get_all(self, ids: Optional[list[int]] = None) -> list[User]:
        """
        Gets all users or users by their IDs.

        :return: A list of all users or users by their IDs.
        :rtype: list[User]
        """
        if not ids:
            users = await self._get_all()
        else:
            users = (await self.session.scalars(select(self._model).where(self._model.id.in_(ids)))).all()
        return [user.to_entity() for user in users]

    async def to_admins(self, user_ids: list[int]) -> bool:
        """
        Changes a users to an admins.

        :param user_ids: The IDs of the users to change.
        :type user_ids: List[int]

        :return: True if the users was changed to an admin, False otherwise.
        :rtype: bool
        """
        stmt = (
            update(self._model)
            .where(self._model.id.in_(user_ids))
            .values(is_admin=True)
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def to_superusers(self, user_ids: list[int]) -> bool:
        """
        Changes a users to an superusers.

        :param user_ids: The IDs of the users to change.
        :type user_ids: List[int]

        :return: True if the users was changed to an superusers, False otherwise.
        :rtype: bool
        """
        stmt = (
            update(self._model)
            .where(self._model.id.in_(user_ids))
            .values(is_admin=True, is_superuser=True)
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0
