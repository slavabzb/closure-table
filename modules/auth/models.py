import logging
import sqlalchemy as sa
from aiohttp_security import CookiesIdentityPolicy
from aiohttp_security import setup as setup_security

from .policy import DBAuthorizationPolicy

__all__ = ["setup_models"]

metadata = sa.MetaData()

users = sa.Table(
    'users', metadata,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('login', sa.String(256), nullable=False),
    sa.Column('passwd', sa.String(256), nullable=False),
    sa.Column('is_superuser', sa.Boolean, nullable=False,
              server_default='FALSE'),
    sa.Column('disabled', sa.Boolean, nullable=False,
              server_default='FALSE'),

    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('login', name='user_login_key'),
)

permissions = sa.Table(
    'permissions', metadata,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('user_id', sa.Integer, nullable=False),
    sa.Column('perm_name', sa.String(64), nullable=False),

    sa.PrimaryKeyConstraint('id', name='permission_pkey'),
    sa.ForeignKeyConstraint(['user_id'], [users.c.id],
                            name='user_permission_fkey',
                            ondelete='CASCADE'),
)


async def setup_models(app):
    setup_security(app, CookiesIdentityPolicy(),
                   DBAuthorizationPolicy(app["db"]))
    logger = logging.getLogger(__name__)
    async with app["db"].acquire() as cnx:
        async with cnx.begin():
            query = """CREATE TABLE IF NOT EXISTS users
            (
              id integer NOT NULL,
              login character varying(256) NOT NULL,
              passwd character varying(256) NOT NULL,
              is_superuser boolean NOT NULL DEFAULT false,
              disabled boolean NOT NULL DEFAULT false,
              CONSTRAINT user_pkey PRIMARY KEY (id),
              CONSTRAINT user_login_key UNIQUE (login)
            )"""
            logger.debug(query)
            await cnx.execute(query)

            query = """CREATE TABLE IF NOT EXISTS permissions
            (
              id integer NOT NULL,
              user_id integer NOT NULL,
              perm_name character varying(64) NOT NULL,
              CONSTRAINT permission_pkey PRIMARY KEY (id),
              CONSTRAINT user_permission_fkey FOREIGN KEY (user_id)
                  REFERENCES users (id) MATCH SIMPLE
                  ON UPDATE NO ACTION ON DELETE CASCADE
            )"""
            logger.debug(query)
            await cnx.execute(query)

            query = """INSERT INTO users(
            id, login, passwd, is_superuser, disabled
            ) VALUES (
            1, 'admin',
            '$5$rounds=535000$aFVGoQluu./5.Rar$nocnwbucnNpUGXRKRnSOEJav.HMxZzvyK.uR0Kyg/Z2',
            TRUE, FALSE
            ) ON CONFLICT (id) DO NOTHING"""
            logger.debug(query)
            await cnx.execute(query)
