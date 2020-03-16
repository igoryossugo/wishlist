from dataclasses import asdict, dataclass, field

from simple_settings import settings

from genie.backends.pools import DatabaseBackendPool


@dataclass
class BaseModel:
    pk: int = field(default=False, init=False)

    @property
    def table_name(self):
        return self.__class__.__name__

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

    def save(self):
        return self.connection().save(**self.to_dict())

    def update(self, **kwargs):
        return self.connection().update(id=self.pk, **kwargs)

    def to_dict(self):
        return asdict(self)
