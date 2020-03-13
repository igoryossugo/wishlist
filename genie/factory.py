from aiohttp import web


def build_app():
    pre_startup()
    app = web.Application()
    app.on_startup.append(start_plugins)
    app.on_cleanup.append(stop_plugins)
    setup_routes()
    return app


def pre_startup():
    pass


def setup_routes():
    pass


async def start_plugins(app):
    pass


async def stop_plugins(app):
    pass
