from typing import Dict, Optional
from uuid import uuid4

from dataclasses import dataclass

from genie.backends.database.models import BaseModel
from genie.customer.exceptions import CustomerAlreadyExists


@dataclass
class CustomerModel(BaseModel):
    table_name = 'CustomerModel'

    name: str
    email: str
    id: str = None
    wishlist_id: Optional[str] = None

    @classmethod
    def get(cls, **kwargs):
        customer = super().get(**kwargs)
        return cls.from_dict(customer)

    def save(self, wishlist_id: str = None):
        if wishlist_id:
            self.wishlist_id = wishlist_id

        super().save()

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            wishlist_id=data['wishlist_id'],
        )


class Customer:

    def __init__(self, id: str, name: str = None, email: str = None):
        self.model = CustomerModel(id=id, name=name, email=email)

    @classmethod
    def create(cls, name: str, email: str):
        customer = CustomerModel.get(email=email)
        if customer:
            CustomerAlreadyExists

        return cls(id=uuid4(), name=name, email=email)

    async def get(self) -> CustomerModel:
        self.model = CustomerModel.get(id=self.model.id)
        await self.save()
        return self.model

    async def save(self):
        return self.model.save()

    async def update(self, customer: CustomerModel):
        self.model = customer
        self.save()

    async def delete(self):
        self.model.delete(id=self.model.id)

    def to_dict(self):
        return self.model.to_dict()
