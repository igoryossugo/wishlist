from dataclasses import dataclass

from genie.models import BaseModel


@dataclass
class Wishlist(BaseModel):
    id: str


@dataclass
class WishlistProduct(BaseModel):
    sku: str
    title: str
    image_url: str
    catalog_price: str
    brand: str
    review_score: float
