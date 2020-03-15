from dataclasses import asdict, dataclass

from genie.models.connection import Connection


@dataclass
class BaseModel:

    @property
    def table_name(self):
        return self.__class__.__name__

    @property
    def connection(self):
        return Connection(table_name=self.table_name)

    def to_dict(self):
        return asdict(self)
