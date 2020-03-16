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

        query = f'SELECT * FROM {self._table_name} WHERE {key} = ?'

        result = self._execute(query=query, parameters=(kwargs[key]))
        if result is None:
            raise Exception

        return result

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
        query = f'DELETE FROM {self._table_name} WHERE {key} = ?'

        self._execute(query=query, parameters=(kwargs[key]))

    def update(self, id, **kwargs):
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
