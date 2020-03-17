from decimal import Decimal

from genie.backends.catalog.models import Item


def fake_item(sku=None):
    sku = sku or 'eaefc867-10a6-3a5e-947d-43a984964fcf'
    return Item(
        sku=sku,
        title='Jogo de Cama / Lençol Solteiro Percal 200 Sophia',
        price=Decimal('241.55'),
        image_url=(
            'http://challenge-api.luizalabs.com/images/'
            'eaefc867-10a6-3a5e-947d-43a984964fcf.jpg'
        ),
        brand='artex',
    )


def fake_list_items():
    return [
        Item(
            sku='eaefc867-10a6-3a5e-947d-43a984964fcf',
            title='Jogo de Cama / Lençol Solteiro Percal 200 Sophia',
            price=Decimal('241.55'),
            image_url=(
                'http://challenge-api.luizalabs.com/images/'
                'eaefc867-10a6-3a5e-947d-43a984964fcf.jpg'
            ),
            brand='artex',
        ),
        Item(
            sku='e9a72482-7e95-44ff-ea5a-75147aef2184',
            title='Guitarra Telecaster Fender Standard',
            price=Decimal('7999.9'),
            image_url=(
                'http://challenge-api.luizalabs.com/images/'
                'e9a72482-7e95-44ff-ea5a-75147aef2184.jpg'
            ),
            brand='fender',
            review_score=4.3
        ),
        Item(
            sku='1bcd1b21-7205-4f02-227f-4c8c9e845ade',
            title='Farol Automotivo Lado Direito para Corsa 94 a 2000',
            price=Decimal('147.19'),
            image_url=(
                'http://challenge-api.luizalabs.com/images/'
                '1bcd1b21-7205-4f02-227f-4c8c9e845ade.jpg'
            ),
            brand='nino',
        ),
        Item(
            sku='1c95d400-9847-eda3-de07-0e62d80a30c6',
            title='Guitarra Strato Fender Amercian Special HSS',
            price=Decimal('12719.9'),
            image_url=(
                'http://challenge-api.luizalabs.com/images/'
                '1c95d400-9847-eda3-de07-0e62d80a30c6.jpg'
            ),
            brand='fender',
        )
    ]
