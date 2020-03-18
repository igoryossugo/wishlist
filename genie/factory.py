from aiohttp import web

from genie.customer.urls import build_urls as customer_urls
from genie.wishlist.urls import build_urls as wishlist_urls


def build_app():
    pre_startup()
    app = web.Application()
    app.on_startup.append(start_plugins)
    app.on_cleanup.append(stop_plugins)
    setup_routes(app)
    return app


def pre_startup():
    pass


def setup_routes(app):
    app.add_routes(customer_urls(prefix='/customer'))
    app.add_routes(wishlist_urls(prefix='/wishlist'))


async def start_plugins(app):
    pass


async def stop_plugins(app):
    pass
