import sqlalchemy as sa

meta = sa.MetaData()

document = sa.Table(
    'document', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('text', sa.UnicodeText)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    document.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    document.drop()
