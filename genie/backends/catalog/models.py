from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Item:
    sku: str
    title: str
    price: Decimal
    image_url: str
    brand: str
    review_score: float
