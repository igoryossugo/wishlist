from decimal import Decimal

import pytest

from genie.backends.catalog.models import Item
from genie.customer.models import CustomerModel
from genie.wishlist.models.item import ItemModel


@pytest.fixture
def item_model():
    return ItemModel(
        sku='82727b28-d6b3-813c-5139-50d3b28c16d4',
        title='Alcool em gel',
        image_url=(
            'http://challenge-api.luizalabs.com/images/'
            '82727b28-d6b3-813c-5139-50d3b28c16d4.jpg'
        ),
        price=Decimal('34.9'),
        brand='epoch magia',
        review_score=4.3
    )


@pytest.fixture
def item():
    return Item(
        sku='82727b28-d6b3-813c-5139-50d3b28c16d4',
        title='Alcool em gel',
        image_url=(
            'http://challenge-api.luizalabs.com/images/'
            '82727b28-d6b3-813c-5139-50d3b28c16d4.jpg'
        ),
        price=Decimal('34.9'),
        brand='epoch magia',
        review_score=4.3
    )


@pytest.fixture
def customer_model():
    return CustomerModel(
        id='abc',
        name='Bruneira da Silva',
        email='teste@magazineluiza.com.br',
    )
