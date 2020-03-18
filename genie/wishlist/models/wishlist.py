from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import uuid4

from genie.backends.database.models import BaseModel
from genie.backends.pools.catalog import CatalogBackendPool
from genie.customer.models import CustomerModel
from genie.wishlist.exceptions import WishlistAlreadyExistsForCustomer
from genie.wishlist.models.item import ItemModel


@dataclass
class WishlistModel(BaseModel):
    table_name = 'Wishlist'

    id: str
    items: Optional[List[ItemModel]]

    @classmethod
    def get(cls, id: str):
        items = ItemModel.get(wishlist_id=id)
        return cls(id=id, items=items)

    def add_item(self, item: ItemModel):
        self.items = self.items or []
        self.items.append(item)

    def remove_item(self, sku: str):
        self.items = self.items or []
        new_items = [item for item in self.items if sku != item.sku]
        self.items = new_items

    def save(self):
        self.items = self.items or []
        for item in self.items:
            item.save(wishlist_id=self.id)

        super().save()

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(id=data['id'])


class Wishlist:

    cache = None

    def __init__(self, wishlist_id: str):
        self.model = WishlistModel(id=wishlist_id)

    @classmethod
    def create(cls, customer_id: str) -> WishlistModel:
        customer = CustomerModel.get(customer_id=customer_id)
        if customer.wishlist_id:
            raise WishlistAlreadyExistsForCustomer(error_detail={
                'wishlist_id': customer.wishlist_id
            })

        return cls(wishlist_id=uuid4())

    async def get(self) -> WishlistModel:
        wishlist = self.cache.get(self.model.id)
        if wishlist:
            return WishlistModel.from_dict(self.model.id)

        self.model = WishlistModel.get(id=self.model.id)
        self._reload_items()

    async def save(self):
        self.cache.set(self.model.id, self.to_dict())
        return self.model.save()

    async def add_item(self, sku: str):
        item = self._get_item(sku=sku)
        item_model = ItemModel(
            sku=item.sku,
            title=item.title,
            image_url=item.image_url,
            catalog_price=item.price,
            brand=item.brand,
            review_score=item.review_score
        )
        self.model.add_item(item_model)
        self.save()

    async def remove_item(self, sku: str):
        self.model.remove_item(sku=sku)
        self.save()

    async def _get_item(self, sku):
        catalog_backend = CatalogBackendPool.get_default()
        return await catalog_backend.get_item(sku=sku)

    async def _reload_items(self):
        items = self.model.items
        if not items:
            return

        updated_items = []
        for item in items:
            try:
                new_item = await self._get_item(sku=item.sku)
                updated_items.append(new_item)
            except Exception:
                pass

        self.model.items = updated_items
        self.save()

    def to_dict(self):
        return self.model.to_dict()
