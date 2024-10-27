from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from username_checker.core.entities.user import User
    from username_checker.core.entities.username import Username

SubscriptionIdGenerator = Callable[[], UUID]


class Interval(Enum):

    """Represents a time interval."""

    MINUTE = "1m"
    MINUTE_30 = "30m"
    HOUR = "1h"
    DAY = "1d"


@dataclass
class Subscription:

    """Represents a subscription"""

    id: UUID
    username: "Username"
    interval: Interval
    subscriber: "User"
