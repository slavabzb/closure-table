import sqlalchemy as sa

meta = sa.MetaData()

users = sa.Table(
    'auth_users', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('email', sa.String, nullable=False, unique=True),
    sa.Column('password', sa.String, nullable=False),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users.drop()
