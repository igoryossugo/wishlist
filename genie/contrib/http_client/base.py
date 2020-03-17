import json
from typing import Dict
from urllib.parse import urlencode

import aiohttp


class BaseHttpClient:
    base_url = ''
    default_timeout = None
    encoder = staticmethod(json.dumps)

    async def fetch(
        self,
        method: str,
        route_url: str,
        data: Dict = None,
        query_strings: Dict = None,
        headers: Dict = None,
        timeout: int = None,
        **kwargs,
    ):
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self._build_timeout(timeout)),
        ) as session:
            async with session.request(
                method=method,
                url=self._build_url(route_url, query_strings),
                data=self.encode_body(data),
                headers=self._build_headers(headers)
            ) as response:
                return await self.parse_response(response)

    async def parse_response(self, response):
        return response

    async def get(
        self,
        route_url: str,
        query_strings: Dict = None,
        headers: Dict = None,
        timeout: int = None,
        **kwargs,
    ):
        return await self.fetch(
            method='GET',
            route_url=route_url,
            query_strings=query_strings,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    async def post(
        self,
        route_url: str,
        data: Dict = None,
        query_strings: Dict = None,
        headers: Dict = None,
        timeout: int = None,
        **kwargs,
    ):
        return await self.fetch(
            method='POST',
            route_url=route_url,
            data=data,
            query_strings=query_strings,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    async def patch(
        self,
        route_url: str,
        data: Dict = None,
        query_strings: Dict = None,
        headers: Dict = None,
        timeout: int = None,
        **kwargs,
    ):
        return await self.fetch(
            method='PATCH',
            route_url=route_url,
            data=data,
            query_strings=query_strings,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    async def put(
        self,
        route_url: str,
        data: Dict = None,
        query_strings: Dict = None,
        headers: Dict = None,
        timeout: int = None,
        **kwargs,
    ):
        return await self.fetch(
            method='PUT',
            route_url=route_url,
            data=data,
            query_strings=query_strings,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    async def delete(
        self,
        route_url: str,
        data: Dict = None,
        query_strings: Dict = None,
        headers: Dict = None,
        timeout: int = None,
        **kwargs,
    ):
        return await self.fetch(
            method='DELETE',
            route_url=route_url,
            data=data,
            query_strings=query_strings,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def encode_body(self, data: Dict) -> str:
        if data is None:
            return

        return self.encoder(data)

    def get_default_headers(self) -> Dict:
        return {}

    def _build_timeout(self, timeout: int = None) -> int:
        return self.default_timeout if None else timeout

    def _build_url(self, route_url: str, query_strings: Dict = None):
        url = f'{self.base_url}/{route_url}'
        if query_strings:
            url = f'{url}?{urlencode(query_strings)}'

        return url

    def _build_headers(self, headers: Dict = None) -> Dict:
        headers = headers or {}
        headers.update(self.get_default_headers())
        return headers
