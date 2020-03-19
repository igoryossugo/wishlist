from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from genie.backends.database.models import BaseModel


@dataclass
class ItemModel(BaseModel):
    table_name = 'WishlistItem'

    sku: str
    title: str
    image_url: str
    price: Decimal
    brand: str
    review_score: Optional[float] = None

    def save(self, wishlist_id):
        super().save(wishlist_id=wishlist_id)
