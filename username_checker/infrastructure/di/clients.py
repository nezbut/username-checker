from collections.abc import AsyncIterable

from cachetools import TTLCache
from dishka import Provider, Scope, provide

from username_checker.common.settings.models import cache
from username_checker.infrastructure.clients.cache.base import BaseCacheClient
from username_checker.infrastructure.clients.cache.ttl_cache import TTLCacheClient


class ClientsProvider(Provider):

    """Clients provider."""

    scope = Scope.APP

    @provide
    async def get_cache_client(self, settings: cache.CacheClientSettings) -> AsyncIterable[BaseCacheClient]:
        """Get the cache client."""
        match settings.client_type:
            case cache.CacheClientType.TTLCACHE:
                ttl_cache: TTLCache = TTLCache(
                    maxsize=float(settings.ttl_cache.maxsize),
                    ttl=float(settings.ttl_cache.ttl),
                )
                client = TTLCacheClient(ttl_cache)
        yield client
        await client.close()


def get_clients_providers() -> list[Provider]:
    """Returns a clients providers for di."""
    return [
        ClientsProvider(),
    ]
