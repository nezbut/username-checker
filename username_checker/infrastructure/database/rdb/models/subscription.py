from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from username_checker.core.entities.subscription import Interval, Subscription
from username_checker.infrastructure.database.rdb.models.base import Base, id_uuid

if TYPE_CHECKING:
    from username_checker.infrastructure.database.rdb.models.user import UserORM
    from username_checker.infrastructure.database.rdb.models.username import UsernameORM


class SubscriptionORM(Base[Subscription]):

    """Represents a subscription in the database."""

    __tablename__ = "subscription"

    id: Mapped[id_uuid]
    interval: Mapped[Interval] = mapped_column(
        Enum(Interval, name="check_int"), nullable=False)

    subscriber_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    subscriber: Mapped["UserORM"] = relationship(
        back_populates="subscriptions",
    )

    username_id: Mapped[UUID] = mapped_column(ForeignKey("username.id"))
    username: Mapped["UsernameORM"] = relationship(
        back_populates="subscriptions",
    )

    def to_entity(self) -> Subscription:
        """
        Converts the current object to a Subscription entity.

        :param self: The current object to be converted.
        :return: The Subscription entity representation of the current object.
        """
        return Subscription(
            id=self.id,
            username=self.username.to_entity(),
            interval=self.interval,
            subscriber=self.subscriber.to_entity(),
        )
