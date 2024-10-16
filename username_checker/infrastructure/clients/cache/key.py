from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class CacheKey(ABC):

    """A class representing a cache key."""

    _prefix: str = "cache"
    _separator: str = ":"

    def build(self) -> str:
        """
        returns the cache key.

        :return: The cache key.
        :rtype: str
        """
        data = [str(value) for value in self._get_key_data()]
        key = self._separator.join(data)
        return f"{self._prefix}{self._separator}{key}"

    @abstractmethod
    def _get_key_data(self) -> list[Any]:
        """
        a list of values for the key is returned.

        :return: The cache key data.
        :rtype: list[Any]
        """
        raise NotImplementedError


@dataclass
class UserCacheKey(CacheKey):

    """A class representing a user cache key."""

    user_id: int

    def _get_key_data(self) -> list[Any]:
        return [self.user_id]
