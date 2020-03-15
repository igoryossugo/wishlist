from dataclasses import dataclass
from unittest import mock

import pytest

from genie.models.base import BaseModel
from genie.models.connection import Connection


class TestBaseModel:

    @pytest.fixture
    def model(self):
        @dataclass
        class TestModel(BaseModel):
            name: str

        return TestModel(name='test')

    def test_connection_returns_instance(self, model):
        assert isinstance(model.connection(), Connection)

    def test_to_dict_calls_asdict(self, model):
        with mock.patch('genie.models.base.asdict') as mock_asdict:
            model.to_dict()

        mock_asdict.assert_called_with(model)

    def test_table_name_returns_class_name(self, model):
        assert model.table_name == 'TestModel'

    def test_get_calls_connection(self, model):
        with mock.patch('genie.models.base.Connection.get') as connection:
            BaseModel.get(a='a', b='b')

        connection.assert_called_with(a='a', b='b')

    def test_delete_calls_connection(self, model):
        with mock.patch('genie.models.base.Connection.delete') as connection:
            BaseModel.delete(a='a')

        connection.assert_called_with(a='a')

    def test_save_calls_connection(self, model):
        with mock.patch('genie.models.base.Connection.save') as connection:
            model.save()

        connection.assert_called_with(**model.to_dict())
