import sqlalchemy as sa

meta = sa.MetaData()

documents = sa.Table(
    'documents', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('text', sa.UnicodeText)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    documents.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    documents.drop()
