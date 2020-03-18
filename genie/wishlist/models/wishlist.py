from dataclasses import dataclass
from simple_settings import settings
from typing import Dict, List, Optional
from uuid import uuid4

from genie.backends.catalog.models import Item
from genie.backends.database.models import BaseModel
from genie.backends.pools.catalog import CatalogBackendPool
from genie.contrib.caches import Cache
from genie.customer.models import CustomerModel
from genie.wishlist.exceptions import WishlistAlreadyExistsForCustomer
from genie.wishlist.models.item import ItemModel


@dataclass
class WishlistModel(BaseModel):
    table_name = 'Wishlist'

    id: str
    items: Optional[List[ItemModel]] = None

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
        return cls(id=data['id'], items=data.get('items'))


class Wishlist:

    def __init__(self, wishlist_id: str):
        self.model = WishlistModel(id=wishlist_id)
        self._cache = Cache()

    @classmethod
    def create(cls, customer_id: str) -> WishlistModel:
        customer = CustomerModel.get(customer_id=customer_id)
        if customer.wishlist_id:
            raise WishlistAlreadyExistsForCustomer(error_detail={
                'wishlist_id': customer.wishlist_id
            })

        return cls(wishlist_id=uuid4())

    async def get(self) -> WishlistModel:
        wishlist = await self._cache.get(self.model.id)
        if wishlist:
            return WishlistModel.from_dict(wishlist)

        self.model = WishlistModel.get(id=self.model.id)
        await self._reload_items()
        return self.model

    async def save(self):
        await self._cache.set(
            self.model.id,
            self.to_dict(),
            settings.WISHLIST_CACHE_MAX_AGE
        )
        return self.model.save()

    async def add_item(self, sku: str):
        item = await self._get_item(sku=sku)
        item_model = self._build_item_model(item=item)
        self.model.add_item(item_model)
        await self.save()

    async def remove_item(self, sku: str):
        self.model.remove_item(sku=sku)
        await self.save()

    async def _get_item(self, sku):
        catalog_backend = CatalogBackendPool.get_default()
        return await catalog_backend.get_item(sku=sku)

    def _build_item_model(self, item: Item) -> ItemModel:
        return ItemModel(
            sku=item.sku,
            title=item.title,
            image_url=item.image_url,
            price=item.price,
            brand=item.brand,
            review_score=item.review_score
        )

    async def _reload_items(self):
        items = self.model.items
        if not items:
            return

        updated_items = []
        for item in items:
            try:
                new_item = await self._get_item(sku=item.sku)
                updated_items.append(self._build_item_model(item=new_item))
            except Exception:
                pass

        self.model.items = updated_items
        await self.save()

    def to_dict(self):
        return self.model.to_dict()
