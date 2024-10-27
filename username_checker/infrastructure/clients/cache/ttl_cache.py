from typing import Any

from cachetools import TTLCache

from username_checker.infrastructure.clients.cache.base import BaseCacheClient
from username_checker.infrastructure.clients.cache.key import CacheKey


class TTLCacheClient(BaseCacheClient):

    """
    A client for interacting with a TTL (Time-To-Live) cache.

    This class provides methods for getting, setting, and deleting values from a TTL cache.
    """

    def __init__(self, cache: TTLCache):
        self.cache = cache

    async def get(self, key: CacheKey) -> Any:
        """
        Retrieves a value from the cache by its key.

        :param key: The key of the value to be retrieved.
        :type key: CacheKey
        :return: The value associated with the given key.
        :rtype: Any
        """
        get_key = key.build()
        return self.cache.get(get_key)

    async def set(self, key: CacheKey, value: Any) -> None:
        """
        Sets a value in the cache by its key.

        :param key: The key of the value to be set.
        :type key: CacheKey
        :param value: The value to be set.
        :type value: Any
        :return: None
        """
        set_key = key.build()
        self.cache[set_key] = value

    async def delete(self, key: CacheKey) -> None:
        """
        Deletes a value from the cache by its key.

        :param key: The key of the value to be deleted.
        :type key: CacheKey
        :return: None
        """
        del_key = key.build()
        self.cache.pop(del_key, None)

    async def close(self) -> None:
        """
        Closes the cache client.

        :return: None
        """
        pass
