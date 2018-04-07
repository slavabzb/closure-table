import click
from aiohttp import web


async def index(request):
    return web.Response(text='index')


@click.group()
def cli():
    pass


@cli.command()
def serve():
    app = web.Application()
    app.router.add_get('/', index)
    web.run_app(app)
