from dataclasses import dataclass
from unittest import mock

import pytest

from genie.models.base import BaseModel, Connection


class TestBaseModel:

    @pytest.fixture
    def model(self):
        @dataclass
        class TestModel(BaseModel):
            name: str

        return TestModel(name='test')

    def test_connection_returns_instance(self, model):
        assert isinstance(model.connection, Connection)

    def test_to_dict_calls_asdict(self, model):
        with mock.patch('genie.models.base.asdict') as mock_asdict:
            model.to_dict()

        mock_asdict.assert_called_with(model)

    def test_table_name_returns_class_name(self, model):
        assert model.table_name == 'TestModel'
