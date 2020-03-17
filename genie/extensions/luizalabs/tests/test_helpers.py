from decimal import Decimal

import pytest

from genie.backends.catalog.models import Item
from genie.extensions.luizalabs.helpers import build_item_response


class TestHelper:

    @pytest.fixture
    def response_item(self):
        return {
            'id': '82727b28-d6b3-813c-5139-50d3b28c16d4',
            'image': (
                'http://challenge-api.luizalabs.com/images/'
                '82727b28-d6b3-813c-5139-50d3b28c16d4.jpg'
            ),
            'price': 34.9,
            'brand': 'epoch magia',
            'title': 'Sylvanian Families Conjunto de Piano',
            'reviewScore': 4.3
        }

    def test_build_item_response_returns_item(self, response_item):
        item = build_item_response(response_item)
        assert isinstance(item, Item)
        assert item.sku == response_item['id']
        assert item.image_url == response_item['image']
        assert item.price == Decimal(response_item['price'])
        assert item.brand == response_item['brand']
        assert item.title == response_item['title']
        assert item.review_score == response_item['reviewScore']

    def test_build_item_response_without_review_returns_item(
        self,
        response_item
    ):
        del(response_item['reviewScore'])
        item = build_item_response(response_item)
        assert isinstance(item, Item)
        assert item.sku == response_item['id']
        assert item.image_url == response_item['image']
        assert item.price == Decimal(response_item['price'])
        assert item.brand == response_item['brand']
        assert item.title == response_item['title']
        assert item.review_score is None
