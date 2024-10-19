from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from username_checker.infrastructure.database.rdb.models.base import Base


class AssociationUsernameUser(Base[None]):

    """Represents an association between a username and a user."""

    __tablename__ = "username_user_assoc"

    username_id: Mapped[UUID] = mapped_column(
        ForeignKey("username.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True,
    )

    def to_entity(self) -> None:
        """No entity."""
