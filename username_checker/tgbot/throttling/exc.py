from time import time
from typing import Any

from username_checker.tgbot.throttling import constant


class ThrottledError(Exception):

    """Exception raised when a rate limit is exceeded."""

    def __init__(self, **kwargs: Any) -> None:
        self.called_at = kwargs.pop(constant.LAST_CALL_KEY, time())
        self.rate = kwargs.pop(constant.RATE_LIMIT_KEY, None)
        self.exceeded_count = kwargs.pop(constant.EXCEEDED_COUNT_KEY, 0)
        self.delta = kwargs.pop(constant.DELTA_KEY, 0)
        self.user = kwargs.pop("user", None)
        self.chat = kwargs.pop("chat", None)

    def __str__(self) -> str:
        """Returns a string"""
        return f"Rate limit exceeded! (Limit: {self.rate} s, exceeded: {self.exceeded_count}, time delta: {round(self.delta, 3)} s)"


class CancelHandlerError(Exception):

    """Exception raised when a cancel handler is called."""

    pass
