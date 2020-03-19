from dataclasses import asdict, dataclass, field

from simple_settings import settings

from genie.backends.pools import DatabaseBackendPool


@dataclass
class BaseModel:

    pk: int = field(default=False, init=False)

    @classmethod
    def connection(cls):
        return DatabaseBackendPool.get(
            backend_id=settings.DEFAULT_DATABASE_BACKEND,
            table_name=cls.table_name
        )

    @classmethod
    def get(cls, **kwargs):
        return cls.connection().get(**kwargs)

    @classmethod
    def delete(cls, **kwargs):
        return cls.connection().delete(**kwargs)

    def save(self, **kwargs):
        kwargs = kwargs or {}
        kwargs.update(self.to_dict())
        return self.connection().save(**kwargs)

    def update(self):
        return self.connection().update(id=self.pk, **self.to_dict())

    def to_dict(self):
        response = asdict(self)
        del(response['pk'])
        return response
