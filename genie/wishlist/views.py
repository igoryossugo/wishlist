import logging

from aiohttp import web
from marshmallow import ValidationError

from genie.contrib.response import JSONResponse
from genie.wishlist.models.wishlist import Wishlist
from genie.wishlist.schemas import WishlistSchema

logger = logging.getLogger(__name__)


def _get_wishlist_id(request):
    return request.match_info['wishlist_id']


def _get_sku(request):
    return request.match_info['sku']


class CreateWishlistView(web.View):

    async def post(self):
        data = await self.request.json()
        schema = WishlistSchema(strict=True)
        try:
            schema = schema.load(data)
        except ValidationError as e:
            logger.debug(
                f'Error validating wishlist create. Error {e.messages}'
            )
            return JSONResponse(
                data={'error_message': e.messages},
                status=400
            )

        wishlist = Wishlist.create(customer_id=schema.customer_id)

        return JSONResponse(status=201, data=wishlist.to_dict())


class GetWishlistView(web.View):

    async def get(self):
        wishlist_id = _get_wishlist_id(self.request)
        wishlist = Wishlist(wishlist_id=wishlist_id).get()
        return JSONResponse(status=200, data=wishlist.to_dict())


class ItemWishlist(web.View):

    async def put(self):
        wishlist_id = _get_wishlist_id(self.request)
        sku = _get_sku(self.request)

        wishlist = Wishlist.get(id=wishlist_id)
        wishlist.add_item(sku=sku)

        return JSONResponse(status=200, data=wishlist.to_dict())

    async def delete(self):
        wishlist_id = _get_wishlist_id(self.request)
        sku = _get_sku(self.request)

        wishlist = Wishlist.get(id=wishlist_id)
        wishlist.remove_item(sku=sku)

        return JSONResponse(status=200, data=wishlist.to_dict())
