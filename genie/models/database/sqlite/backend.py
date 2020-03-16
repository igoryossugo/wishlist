import sqlite3

from ramos.mixins import ThreadSafeCreateMixin

from genie.backends.database.backend import DatabaseBackend

_con = sqlite3.connect(":memory:")


class SqliteDatabaseBackend(DatabaseBackend, ThreadSafeCreateMixin):
    id = 'sqlite'
    name = 'Sqlite Database'
    _connection = _con

    def _get(self, **kwargs):
        if not kwargs:
            raise ValueError

        key = list(kwargs.keys())[0]

        query = f'SELECT * FROM {self._table_name} WHERE {key} = ?'

        result = self._execute(query=query, parameters=(kwargs[key]))
        if result is None:
            raise Exception

        return result

    def _save(self, **kwargs):
        if not kwargs:
            raise ValueError

        query_columns, query_values = None, None

        columns = list(kwargs.keys())
        for column in columns:
            if not query_columns:
                query_columns = f'{column}'
                query_values = '?'
                continue

            query_columns = f'{query_columns}, {column}'
            query_values = f'{query_values}, ?'

        query = f"""
            INSERT INTO {self._table_name}({query_columns})
            VALUES ({query_values})
        """

        self._execute(query=query, parameters=tuple(kwargs.values()))

    def _delete(self, **kwargs):
        if not kwargs:
            raise ValueError

        key = list(kwargs.keys())[0]
        query = f'DELETE FROM {self._table_name} WHERE {key} = ?'

        self._execute(query=query, parameters=(kwargs[key]))

    def _update(self, id, **kwargs):
        if not kwargs:
            raise ValueError

        query_set = None
        parameters = []

        for key in kwargs:
            parameters.append(kwargs[key])
            if not query_set:
                query_set = f'{key}=?'
                continue

            query_set = f'{query_set}, {key}=?'

        parameters.append(id)
        query = f"""
            UPDATE {self._table_name}
            SET {query_set}
            WHERE id=?
        """
        self._execute(query=query, parameters=tuple(parameters))

    def _execute(self, query, parameters=None):
        cursor = self._connection.cursor()
        cursor.execute(query, parameters)
        result = cursor.fetchall()

        return result
