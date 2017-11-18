import sqlalchemy as sa

meta = sa.MetaData()

comments_tree = sa.Table(
    'comments_tree', meta,
    sa.Column('ancestor_id', sa.Integer, nullable=False),
    sa.Column('descendant_id', sa.Integer, nullable=False),
    sa.Column('level', sa.Integer, nullable=False)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    comments_tree.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    comments_tree.drop()
