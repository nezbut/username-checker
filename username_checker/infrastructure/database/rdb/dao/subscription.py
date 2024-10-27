from typing import Optional
from uuid import UUID

from adaptix import dump
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from username_checker.core.entities.subscription import Subscription
from username_checker.core.entities.user import User
from username_checker.core.entities.username import Username
from username_checker.infrastructure.database.rdb.dao.base import BaseDAO
from username_checker.infrastructure.database.rdb.models import SubscriptionORM


class SubscriptionDAO(BaseDAO[SubscriptionORM]):

    """A class representing the DAO for the Subscription model."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(SubscriptionORM, session)

    async def get_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        """
        Retrieves a subscription by their ID.

        :param subscription_id: The ID of the user to retrieve.
        :type subscription_id: UUID

        :return: The subscription entity.
        :rtype: Subscription
        """
        options = (selectinload(self._model.subscriber),
                   selectinload(self._model.username))
        subscription = await self._get_by_id(subscription_id, options=options)
        return subscription.to_entity() if subscription else None

    async def get_by_username(self, username: Username) -> Optional[Subscription]:
        """
        Gets a subscription by username.

        :param username: The username of the subscription.
        :type username: Username
        :return: The subscription.
        :rtype: Subscription
        """
        stmt = (
            select(self._model)
            .options(
                selectinload(self._model.subscriber),
                selectinload(self._model.username),
            )
            .where(self._model.username_id == username.id)
        )
        result = await self.session.execute(stmt)
        sub = result.scalar_one_or_none()
        if sub is not None:
            return sub.to_entity()
        return sub

    async def get_by_subscriber(self, subscriber: User) -> Optional[Subscription]:
        """
        Get subscription by a subscriber.

        :param user: The user.
        :type user: User
        :return: Subscription by a subscriber.
        :rtype: Subscription
        """
        stmt = (
            select(self._model)
            .options(
                selectinload(self._model.subscriber),
                selectinload(self._model.username),
            )
            .where(self._model.subscriber_id == subscriber.id)
        )
        result = await self.session.execute(stmt)
        sub = result.scalar_one_or_none()
        if sub is not None:
            return sub.to_entity()
        return sub

    async def get_subscriptions(self, subscription_ids: Optional[list[UUID]] = None) -> list[Subscription]:
        """
        Gets all subscriptions or subscriptions by their IDs.

        :param subscription_ids: An optional list of subscription IDs.
        :return: A list of all subscriptions or subscriptions by their IDs.
        """
        options = (selectinload(self._model.subscriber),
                   selectinload(self._model.username))
        if not subscription_ids:
            subscriptions = await self._get_all(options=options)
        else:
            stmt = (
                select(self._model)
                .options(*options)
                .where(self._model.id.in_(subscription_ids))
            )
            subscriptions = (await self.session.scalars(stmt)).all()
        return [subscription.to_entity() for subscription in subscriptions]

    async def upsert(self, subscription: Subscription) -> Subscription:
        """
        Upserts a subscription into the database.

        :param subscription: The subscription to be upserted.
        :type subscription: Subscription

        :return: The upserted subscription.
        :rtype: Subscription
        """
        kwargs = dump(subscription)
        kwargs["interval"] = subscription.interval
        kwargs["subscriber_id"] = kwargs.pop("subscriber")["id"]
        kwargs["username_id"] = kwargs.pop("username")["id"]

        saved_subscription = await self.session.execute(
            insert(self._model)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(
                    self._model.id,), set_=kwargs, where=self._model.id == subscription.id,
            )
            .returning(self._model),
        )
        return saved_subscription.scalar_one().to_entity()

    async def delete(self, subscription_id: UUID) -> bool:
        """
        Deletes a subscription from the database.

        :param subscription_id: The ID of the subscription to be deleted.
        :type subscription_id: UUID
        :return: bool
        """
        stmt = delete(self._model).where(self._model.id == subscription_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
