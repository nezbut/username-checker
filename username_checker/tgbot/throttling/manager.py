from dataclasses import dataclass
from time import time
from typing import Any

from username_checker.infrastructure.clients.cache.base import BaseCacheClient
from username_checker.infrastructure.clients.cache.key import CacheKey
from username_checker.tgbot.throttling import constant
from username_checker.tgbot.throttling.exc import ThrottledError


@dataclass
class BotThrottlingCacheKey(CacheKey):

    """ A class representing a cache key for bot throttling."""

    user_id: int
    chat_id: int
    _prefix: str = "throttle"

    def _get_key_data(self) -> list[Any]:
        return [self.user_id, self.chat_id]


class ThrottleManager:

    """A class responsible for managing rate limiting and throttling for bot interactions."""

    def __init__(self, cache: BaseCacheClient):
        self.cache = cache
        self.bucket_keys = [
            constant.RATE_LIMIT_KEY, constant.DELTA_KEY,
            constant.LAST_CALL_KEY, constant.EXCEEDED_COUNT_KEY,
        ]

    async def throttle(self, rate: float, user_id: int, chat_id: int) -> bool:
        """
        Asynchronously checks if a bot interaction is within the allowed rate limit.

        :param rate: The allowed rate limit in seconds.
        :param user_id: The ID of the user making the interaction.
        :param chat_id: The ID of the chat where the interaction is happening.

        :return: True if the interaction is within the allowed rate limit, False otherwise.
        """
        now = time()
        key = BotThrottlingCacheKey(user_id=user_id, chat_id=chat_id)

        data: dict[str, Any] = await self.cache.get(key)
        data = {
            k: float(v.decode()) if isinstance(v, bytes) else v
            for k, v in data.items()
            if v is not None
        } if data else {}

        called = data.get(constant.LAST_CALL_KEY, now)
        delta = now - called
        result = delta >= rate or delta <= 0

        data[constant.RATE_LIMIT_KEY] = rate
        data[constant.LAST_CALL_KEY] = now
        data[constant.DELTA_KEY] = delta
        if not result:
            data[constant.EXCEEDED_COUNT_KEY] += 1
        else:
            data[constant.EXCEEDED_COUNT_KEY] = 1

        await self.cache.set(key, data)

        if not result:
            raise ThrottledError(chat=chat_id, user=user_id, **data)

        return result is True
