from typing import TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from username_checker.core.entities.user import LanguageLocale, User
from username_checker.infrastructure.database.rdb.models.base import Base, created_now, id_int

if TYPE_CHECKING:
    from username_checker.infrastructure.database.rdb.models.subscription import SubscriptionORM
    from username_checker.infrastructure.database.rdb.models.username import UsernameORM


class UserORM(Base[User]):

    """Represents a user in the database."""

    __tablename__ = "user"

    id: Mapped[id_int]
    username: Mapped[str] = mapped_column(String, nullable=False)
    joined_us: Mapped[created_now]
    last_activity: Mapped[created_now]
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_banned: Mapped[bool] = mapped_column(nullable=False, default=False)
    language: Mapped[LanguageLocale] = mapped_column(
        Enum(LanguageLocale), nullable=False,
    )

    subscriptions: Mapped[list["SubscriptionORM"]] = relationship(
        back_populates="subscriber",
    )
    used_usernames: Mapped[list["UsernameORM"]] = relationship(
        back_populates="used_usernames_by",
        secondary="username_user_assoc",
    )

    def to_entity(self) -> User:
        """To User entity."""
        return User(
            id=self.id,
            username=self.username,
            joined_us=self.joined_us,
            last_activity=self.last_activity,
            language=self.language,
            is_admin=self.is_admin,
            is_superuser=self.is_superuser,
            is_banned=self.is_banned,
        )
