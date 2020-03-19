from aiocache import caches
from aiohttp import web
from simple_settings import settings

from genie.contrib.auth.middlewares import authorization_middleware
from genie.customer.urls import build_urls as customer_urls
from genie.wishlist.urls import build_urls as wishlist_urls


def build_app():
    pre_startup()
    app = web.Application(middlewares=[
        authorization_middleware
    ])
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
    caches.set_config(settings.CACHE)
    app.cache = caches.get('default')


async def stop_plugins(app):
    cache_config = caches.get_config()
    for cache_name in cache_config:
        await caches.get(cache_name).close()
