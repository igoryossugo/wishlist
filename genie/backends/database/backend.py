import abc


class DatabaseBackend(metaclass=abc.ABCMeta):

    def __init__(self, table_name: str):
        self._table_name = table_name

    def get(self, **kwargs):
        return self._get(**kwargs)

    def save(self, **kwargs):
        return self._save(**kwargs)

    def delete(self, **kwargs):
        return self._delete(**kwargs)

    def update(self, id, **kwargs):
        return self._update(id=id, **kwargs)

    def _get(self, **kwargs):
        pass

    def _save(self, **kwargs):
        pass

    def _delete(self, **kwargs):
        pass

    def _update(self, **kwargs):
        pass

    def _execute(self, query, parameters=None):
        pass
