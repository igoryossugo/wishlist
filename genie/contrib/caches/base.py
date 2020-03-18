class InMemoryCache:

    def __init__(self):
        self._db = {}

    async def get(self, key):
        return self._db.get(key)

    async def set(self, key, value, ttl=None):
        self._db[key] = value

    async def clear(self):
        self._db = {}

    async def delete(self, key):
        if key in self._data:
            del self._data[key]

    async def increment(self, key, delta=1):
        value = await self.get(key)

        if not value:
            await self.set(key, delta)
            return delta

        new_value = value + delta
        await self.set(key, new_value)
        return new_value

    def __repr__(self):
        return '<InMemoryCache: {} keys>'.format(len(self._db))


class RedisCache:

    def __init__(self, redis):
        self.redis = redis

    async def increment(self, key, delta=1):
        try:
            return await self.redis.increment(key)
        except KeyError:
            await self.redis.set(key, delta)
            return delta

    async def delete(self, key):
        return await self.redis.delete([key])

    def __getattr__(self, name):
        return getattr(self.redis, name)
