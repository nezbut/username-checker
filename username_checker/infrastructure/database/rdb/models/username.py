from typing import TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from username_checker.core.entities.username import Username, UsernameStatus
from username_checker.infrastructure.database.rdb.models.base import Base, id_uuid

if TYPE_CHECKING:
    from username_checker.infrastructure.database.rdb.models.subscription import SubscriptionORM
    from username_checker.infrastructure.database.rdb.models.user import UserORM


class UsernameORM(Base[Username]):

    """Represents a username in the database."""

    __tablename__ = "username"

    id: Mapped[id_uuid]
    value: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[UsernameStatus] = mapped_column(
        Enum(UsernameStatus),
        nullable=False,
    )

    used_usernames_by: Mapped[list["UserORM"]] = relationship(
        back_populates="used_usernames",
        secondary="username_user_assoc",
    )
    subscriptions: Mapped[list["SubscriptionORM"]] = relationship(
        back_populates="username",
    )

    def to_entity(self) -> Username:
        """To Username entity."""
        return Username(
            id=self.id,
            value=self.value,
            status=self.status,
        )
