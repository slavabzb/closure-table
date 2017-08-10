import aiopg.sa


async def init_pg(app):
    from settings import DATABASE
    engine = await aiopg.sa.create_engine(**DATABASE)
    app["db"] = engine


async def close_pg(app):
    app["db"].close()
    await app["db"].wait_closed()
