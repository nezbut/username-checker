from dataclasses import dataclass, field
from enum import Enum


class CacheClientType(Enum):

    """An enumeration of cache client types."""

    TTLCACHE = "ttlcache"

@dataclass
class TTLCacheClientSettings:

    """A class representing the settings for the TTLCache."""

    ttl: int = 60 * 60 * 2
    maxsize: int = 5000


@dataclass
class CacheClientSettings:

    """A class representing the settings for a cache client."""

    client_type: CacheClientType = CacheClientType.TTLCACHE
    ttl_cache: TTLCacheClientSettings = field(default_factory=lambda: TTLCacheClientSettings())


@dataclass
class CacheSettings:

    """A class representing the settings for cache."""

    client: CacheClientSettings
