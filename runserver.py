import asyncio

from aiohttp import web
from aiohttp_swagger import setup_swagger

import db
from middlewares import setup_middlewares
from modules import documents, auth
from apps import documents
from apps.documents import app as foo_app

from apps import documents


def init(loop):
    app = web.Application(loop=loop)


    app.on_startup.append(db.setup_pg)
    # app.on_startup.append(auth.models.setup_models)
    # app.on_startup.append(documents.models.setup_models)
    app.on_cleanup.append(db.close_pg)

    # auth.routes.setup_routes(app)
    # documents.routes.setup_routes(app)

    documents.init(app)

    setup_middlewares(app)

    # setup_swagger(app)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = init(loop)
    web.run_app(app)
