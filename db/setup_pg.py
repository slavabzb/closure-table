import aiopg.sa

from settings import DATABASE


async def setup_pg(app):
    engine = await aiopg.sa.create_engine(DATABASE)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
