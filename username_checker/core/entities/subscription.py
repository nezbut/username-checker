from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from username_checker.core.entities.user import User
from username_checker.core.entities.username import Username

SubscriptionIdGenerator = Callable[[], UUID]


class Interval(Enum):

    """Represents a time interval."""

    MINUTE_1 = 60
    MINUTE_30 = 1800
    HOUR_1 = 3600
    DAY_1 = 86400


@dataclass
class Subscription:

    """Represents a subscription"""

    id: UUID
    username: Username
    interval: Interval
    subscriber: User
