from dataclasses import dataclass

from genie.models import BaseModel


@dataclass
class Customer(BaseModel):
    id: str
    name: str
    email: str
    wishlist_id: str
