import sqlite3

_con = sqlite3.connect(":memory:")


class Connection:

    _connection = _con

    def __init__(self, table_name: str):
        self._table_name = table_name

    def get(self, **kwargs):
        if not kwargs:
            raise ValueError

        key = list(kwargs.keys())[0]

        query = f'SELECT * FROM {self._table_name} WHERE ? = ?'

        result = self._execute(query=query, parameters=(key, kwargs[key]))
        if result is None:
            raise Exception

        obj, = result
        return obj

    def save(self, **kwargs):
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

    def delete(self, **kwargs):
        if not kwargs:
            raise ValueError

        key = list(kwargs.keys())[0]
        query = f'DELETE FROM {self._table_name} WHERE ? = ?'

        self._execute(query=query, parameters=(key, kwargs[key]))

    def _execute(self, query, parameters=None):
        with self._connection.cursor() as cursor:
            self._connection.execute(query, parameters)
            result = cursor.fetchone()

        return result
