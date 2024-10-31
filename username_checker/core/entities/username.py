from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from uuid import UUID

UsernameIdGenerator = Callable[[], UUID]


class UsernameStatus(str, Enum):

    """Enum representing the status of a username."""

    AVAILABLE = "available"
    NOT_AVAILABLE = "not_available"
    UNKNOWN = "unknown"


@dataclass
class Username:

    """Represents a username."""

    id: UUID
    value: str
    status: UsernameStatus = UsernameStatus.UNKNOWN
