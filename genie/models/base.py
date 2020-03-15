from dataclasses import asdict, dataclass

from genie.models.connection import Connection


@dataclass
class BaseModel:

    @property
    def table_name(self):
        return self.__class__.__name__

    @classmethod
    def connection(cls):
        return Connection(table_name=cls.table_name)

    @classmethod
    def get(cls, **kwargs):
        return cls.connection().get(**kwargs)

    @classmethod
    def delete(cls, **kwargs):
        return cls.connection().delete(**kwargs)

    def save(self):
        return self.connection().save(**self.to_dict())

    def to_dict(self):
        return asdict(self)
