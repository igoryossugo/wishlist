from typing import Optional

from dataclasses import dataclass

from genie.backends.database.models import BaseModel


@dataclass
class Customer(BaseModel):
    id: str
    name: str
    email: str
    wishlist_id: Optional[str] = None
