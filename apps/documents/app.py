import os

from aiohttp_swagger import setup_swagger

from .routes import setup_routes

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))


def init(app):
    setup_routes(app)

    setup_swagger(
        app, swagger_from_file=os.path.join(PATH, 'swagger.yaml'),
        swagger_url='/documents/api/doc'
    )
