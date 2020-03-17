import json
from unittest import mock

import asynctest
import pytest

from genie.contrib.http_client import BaseHttpClient


class DummyHTTPClient(BaseHttpClient):
    base_url = 'https://dummy.com'
    default_timeout = 1

    def get_default_headers(self):
        return {
            'Content-Type': 'application/json',
        }


class TestBaseHTTPClient:

    @pytest.fixture
    def http_client(self):
        return DummyHTTPClient()

    @pytest.mark.parametrize('function,method', (
        ('get', 'GET'),
        ('put', 'PUT'),
        ('post', 'POST'),
        ('patch', 'PATCH'),
        ('delete', 'DELETE'),
    ))
    async def test_should_call_fetch_correctly(
        self,
        http_client,
        function,
        method
    ):
        with mock.patch.object(http_client, 'fetch') as fetch:
            func = getattr(http_client, function)
            await func(
                route_url='abc',
                data={'abc': 1},
                query_strings={'def': 2},
                headers={
                    'Content-Type': 'application/json',
                },
                timeout=20,
                teste=True
            )

        fetch.assert_called_with(
            method=method,
            route_url='abc',
            data={'abc': 1},
            query_strings={'def': 2},
            headers={
                'Content-Type': 'application/json',
            },
            timeout=20,
            teste=True
        )

    async def test_fetch_calls_request_and_parse_response(self, http_client):
        with asynctest.patch('aiohttp.ClientSession') as mock_session_class:
            mock_session = mock_session_class.return_value
            mock_client = mock_session.__aenter__.return_value
            mock_client.request = asynctest.CoroutineMock()
            mock_session_class.return_value.__aexit__.return_value = (
                asynctest.CoroutineMock()
            )
            await http_client.fetch(
                method='GET',
                route_url='abc',
                data={'abc': 1},
                query_strings={'def': 2},
                headers={'Accept': 'application/json; text/html'},
                timeout=20,
                teste=True
            )

        mock_client.request.assert_called_with(
            method='GET',
            url='https://dummy.com/abc?def=2',
            data=json.dumps({'abc': 1}),
            headers={
                'Accept': 'application/json; text/html',
                'Content-Type': 'application/json',
            }
        )
