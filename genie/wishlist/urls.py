from aiohttp import web

from genie.wishlist import views


def build_urls(prefix=''):
    return [
        web.view(
            f'{prefix}/',
            views.CreateWishlistView
        ),
        web.view(
            f'{prefix}/'
            r'{wishlist_id:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}}/',  # noqa
            views.GetWishlistView
        ),
        web.view(
            f'{prefix}/'
            r'{wishlist_id:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}}/'  # noqa
            r'{sku:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}}/',  # noqa
            views.ItemWishlist
        ),
    ]
