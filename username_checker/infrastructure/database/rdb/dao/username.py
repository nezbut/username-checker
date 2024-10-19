from typing import Optional
from uuid import UUID

from adaptix import dump
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from username_checker.core.entities.username import Username
from username_checker.infrastructure.database.rdb.dao.base import BaseDAO
from username_checker.infrastructure.database.rdb.models import UsernameORM


class UsernameDAO(BaseDAO[UsernameORM]):

    """A class representing the DAO for the Username model."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(UsernameORM, session)

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
