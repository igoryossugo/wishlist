from typing import Dict, Optional

from aiocache import caches
from aiocache.base import BaseCache


class Cache:
    def __init__(self, cache: BaseCache = None):
        self._cache = cache or caches.get('default')

    async def get(self, key: str) -> Optional[Dict]:
        return await self._cache.get(self._cache_key(key))

    async def set(self, key: str, data: Dict, ttl: int):
        return await self._cache.set(self._cache_key(key), data, ttl)

    def _cache_key(self, key: str) -> str:
        return f'base-cache-{key}'
