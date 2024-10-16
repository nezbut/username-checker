from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Annotated, Generic, TypeVar
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column

id_int = Annotated[int, mapped_column(BigInteger, primary_key=True)]
id_uuid = Annotated[UUID, mapped_column(primary_key=True)]
created_now = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
]
_EntityType = TypeVar("_EntityType")


class Base(DeclarativeBase, Generic[_EntityType]):

    """Base class for all database models."""

    __metaclass__ = ABCMeta
    repr_cols_num = 2
    repr_cols: tuple = ()

    def __repr__(self) -> str:
        """Returns a string representation of the object."""
        cols = [
            f"{col}={getattr(self, col)}" for index, col in enumerate(self.__table__.columns.keys())
            if col in self.repr_cols or index < self.repr_cols_num
        ]

        return f"{self.__class__.__name__}({', '.join(cols)})"

    @abstractmethod
    def to_entity(self) -> _EntityType:
        """Converts the current database model to entity."""
        raise NotImplementedError
