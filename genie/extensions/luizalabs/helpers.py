from decimal import Decimal

from genie.backends.catalog.models import Item


def build_item_response(response):
    item = Item(
        sku=response['id'],
        title=response['title'],
        price=Decimal(response['price']),
        image_url=response['image'],
        brand=response['brand'],
    )
    if 'reviewScore' in response:
        item.review_score = response['reviewScore']

    return item
