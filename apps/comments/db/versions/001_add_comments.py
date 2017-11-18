import sqlalchemy as sa

meta = sa.MetaData()

comments = sa.Table(
    'comments', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('content', sa.String, nullable=False)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    comments.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    comments.drop()
