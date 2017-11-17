import asyncio

from aiohttp import web

import db
from apps import comments
from middlewares import setup_middlewares


def init(loop):
    app = web.Application(loop=loop)

    app.on_startup.append(db.setup_pg)
    # app.on_startup.append(auth.models.setup_models)
    # app.on_startup.append(comments.models.setup_models)
    app.on_cleanup.append(db.close_pg)

    # auth.routes.setup_routes(app)
    # comments.routes.setup_routes(app)

    comments.setup_app(app)

    setup_middlewares(app)

    # setup_swagger(app)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = init(loop)
    web.run_app(app)
