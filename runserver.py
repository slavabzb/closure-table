import asyncio
import os

import aiopg.sa
from aiohttp import web
from aiohttp_swagger import setup_swagger

from apps import auth, comments
from middlewares import setup_middlewares
from settings import DATABASE

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


async def setup_pg(app):
    engine = await aiopg.sa.create_engine(DATABASE)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


def init(loop):
    app = web.Application(loop=loop)

    app.on_startup.append(setup_pg)
    # app.on_startup.append(auth.models.setup_models)
    # app.on_startup.append(comments.models.setup_models)
    app.on_cleanup.append(close_pg)

    # auth.routes.setup_routes(app)
    auth.routes.setup_routes(app)
    comments.routes.setup_routes(app)

    # setup_middlewares(app)

    setup_swagger(app, swagger_from_file=os.path.join(PATH, 'swagger.yaml'))

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = init(loop)
    web.run_app(app)
