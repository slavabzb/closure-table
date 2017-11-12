import aiopg.sa
import sqlalchemy as sa

from settings import DATABASE

meta = sa.MetaData()

documents = sa.Table(
    'documents', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('text', sa.UnicodeText)
)


async def init_pg(app):
    engine = await aiopg.sa.create_engine(DATABASE)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
