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
    # root user (id == 1): admin/admin with salt == 1
    query = users.insert().values(email='admin', password=(
        '58b5444cf1b6253a4317fe12daff411a78bda0a95279b1d5768ebf5ca60829e7'
        '8da944e8a9160a0b6d428cb213e813525a72650dac67b88879394ff624da482f'
    ))
    with migrate_engine.connect() as conn:
        conn.execute(query)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    query = users.delete().where(users.c.email == 'admin')
    with migrate_engine.connect() as conn:
        conn.execute(query)
