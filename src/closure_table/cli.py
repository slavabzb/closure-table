import click
from aiohttp.web import Application, run_app
from closure_table.setup import setup_app


@click.group()
def cli():
    pass


@cli.command()
def serve():
    app = Application()
    setup_app(app)
    run_app(app)
