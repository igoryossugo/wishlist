from unittest import mock

import pytest

from genie.models.database.sqlite.backend import SqliteDatabaseBackend


class TestSqliteDatabaseBackend:

    @pytest.fixture
    def connection(self):
        return SqliteDatabaseBackend(table_name='TestConnection')

    @pytest.fixture
    def mock_execute(self, connection):
        return mock.patch.object(connection, '_execute')

    def test_get_should_call_execute(self, connection, mock_execute):
        with mock_execute as execute:
            execute.return_value = ({},)
            connection.get(name='test')

        execute.assert_called_with(
            query='SELECT * FROM TestConnection WHERE name = ?',
            parameters=('test')
        )

    def test_insert_should_call_execute(self, connection, mock_execute):
        with mock_execute as execute:
            connection.save(name='test', age=23, email='test@test.com')

        expected_query = """
            INSERT INTO TestConnection(name, age, email)
            VALUES (?, ?, ?)
        """
        execute.assert_called_with(
            query=expected_query,
            parameters=('test', 23, 'test@test.com')
        )

    def test_delete_should_call_execute(self, connection, mock_execute):
        with mock_execute as execute:
            connection.delete(email='test@test.com')

        execute.assert_called_with(
            query='DELETE FROM TestConnection WHERE email = ?',
            parameters=('test@test.com')
        )

    def test_update_should_call_execute(self, connection, mock_execute):
        with mock_execute as execute:
            connection.update(id=123, name='test', email='test@test.com')

        expected_query = """
            UPDATE TestConnection
            SET name=?, email=?
            WHERE id=?
        """
        execute.assert_called_with(
            query=expected_query,
            parameters=('test', 'test@test.com', 123)
        )
