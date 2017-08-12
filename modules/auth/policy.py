import sqlalchemy as sa
from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import sha256_crypt

from . import models


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, dbengine):
        self.dbengine = dbengine

    async def authorized_userid(self, identity):
        async with self.dbengine.acquire() as cnx:
            where = sa.and_(models.users.c.login == identity,
                            sa.not_(models.users.c.disabled))
            query = models.users.count().where(where)
            ret = await cnx.scalar(query)
            if ret:
                return identity
            else:
                return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False

        async with self.dbengine.acquire() as cnx:
            where = sa.and_(models.users.c.login == identity,
                            sa.not_(models.users.c.disabled))
            query = models.users.select().where(where)
            ret = await cnx.execute(query)
            user = await ret.fetchone()
            if user is not None:
                user_id = user[0]
                is_superuser = user[3]
                if is_superuser:
                    return True

                where = models.permissions.c.user_id == user_id
                query = models.permissions.select().where(where)
                ret = await cnx.execute(query)
                result = await ret.fetchall()
                if ret is not None:
                    for record in result:
                        if record.perm_name == permission:
                            return True

            return False


async def check_credentials(db_engine, username, password):
    async with db_engine.acquire() as cnx:
        where = sa.and_(models.users.c.login == username,
                        sa.not_(models.users.c.disabled))
        query = models.users.select().where(where)
        ret = await cnx.execute(query)
        user = await ret.fetchone()
        if user is not None:
            userhash = user[2]
            return sha256_crypt.verify(password, userhash)
    return False
