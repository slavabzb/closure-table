import os

from aiohttp_swagger import setup_swagger
from aiopg import sa
from closure_table import (
    auth,
    comments,
)
from closure_table.settings import DATABASE

BASE_PATH = os.path.abspath(os.path.dirname(__file__))


def setup_app(app):
    # setup_db(app)
    setup_routes(app)
    setup_middlewares(app)
    setup_swagger(app, swagger_from_file=os.path.join(BASE_PATH, 'swagger.yaml'))


def setup_middlewares(app):
    auth.middlewares.setup_middlewares(app)


def setup_routes(app):
    auth.routes.setup_routes(app)
    comments.routes.setup_routes(app)


def setup_db(app):
    app.on_startup.append(setup_pg)
    app.on_cleanup.append(close_pg)


async def setup_pg(app):
    engine = await sa.create_engine(DATABASE)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
