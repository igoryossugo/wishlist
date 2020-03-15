from unittest import mock

import pytest

from genie.models.base import Connection


class TestConnection:

    @pytest.fixture
    def connection(self):
        return Connection(table_name='TestConnection')

    @pytest.fixture
    def mock_execute(self, connection):
        return mock.patch.object(connection, '_execute')

    def test_get_should_call_execute(self, connection, mock_execute):
        with mock_execute as execute:
            execute.return_value = ({},)
            connection.get(name='test')

        execute.assert_called_with(
            query='SELECT * FROM TestConnection WHERE ? = ?',
            parameters=('name', 'test')
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
            query='DELETE FROM TestConnection WHERE ? = ?',
            parameters=('email', 'test@test.com')
        )
