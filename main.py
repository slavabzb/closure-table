import os

import aiopg.sa
import yaml
from aiohttp import web
from aiohttp_swagger import setup_swagger

os.environ.setdefault("DEBUG", "True")

import settings


async def ping(request):
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "pong" text
        "405":
            description: invalid HTTP Method
    """
    return web.Response(text="pong")


async def load_conf(app):
    with open(settings.DB_CONF, "r") as fp:
        conf = yaml.safe_load(fp)
    app["config"] = conf


async def init_pg(app):
    conf = app["config"]
    engine = await aiopg.sa.create_engine(
        database=conf["database"],
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        minsize=conf["minsize"],
        maxsize=conf["maxsize"])
    app["db"] = engine


async def close_pg(app):
    app["db"].close()
    await app["db"].wait_closed()


if __name__ == "__main__":
    app = web.Application()

    app.on_startup.append(load_conf)
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    app.router.add_route("GET", "/ping", ping)

    setup_swagger(app)

    web.run_app(app, host="127.0.0.1")
