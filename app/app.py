import asyncio

from aiohttp import web
from aiohttp_swagger import setup_swagger

import settings
from db import init_pg, close_pg
from middlewares import setup_middlewares
from routes import setup_routes
from utils import load_conf
from .conf import load_app_conf


def init(loop):
    app = web.Application(loop=loop)

    app.on_startup.append(load_app_conf)
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    setup_routes(app)
    setup_middlewares(app)
    setup_swagger(app)

    return app


def run():
    loop = asyncio.get_event_loop()
    app = init(loop)
    web.run_app(app, **load_conf(settings.APP_CONF))
