from dataclasses import dataclass
from enum import Enum


class Interval(Enum):

    """Represents a time interval."""

    MINUTE = "1m"
    MINUTE_30 = "30m"
    HOUR = "1h"
    DAY = "1d"


@dataclass
class Subscription:

    """Represents a subscription"""

    username: str
    interval: Interval
