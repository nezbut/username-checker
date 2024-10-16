from abc import ABC, abstractmethod
from typing import Any

from username_checker.infrastructure.clients.cache.key import CacheKey


class BaseCacheClient(ABC):

    """A base class for cache clients."""

    @abstractmethod
    async def get(self, key: CacheKey) -> Any:
        """
        Retrieves a value from the cache by its key.

        :param key: The key of the value to be retrieved.
        :type key: CacheKey
        :return: The value associated with the given key.
        :rtype: Any
        """
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: CacheKey, value: Any) -> None:
        """
        Sets a value in the cache by its key.

        :param key: The key of the value to be set.
        :type key: CacheKey
        :param value: The value to be set.
        :type value: Any
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: CacheKey) -> None:
        """
        Deletes a value from the cache by its key.

        :param key: The key of the value to be deleted.
        :type key: CacheKey
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        Closes the cache client.

        :return: None
        """
        raise NotImplementedError
