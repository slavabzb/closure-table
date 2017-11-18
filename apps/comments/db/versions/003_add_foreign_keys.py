import sqlalchemy as sa
from migrate.changeset.constraint import ForeignKeyConstraint

meta = sa.MetaData()

comments = sa.Table(
    'comments', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('content', sa.String, nullable=False)
)

comments_tree = sa.Table(
    'comments_tree', meta,
    sa.Column('ancestor_id', sa.Integer, nullable=False),
    sa.Column('descendant_id', sa.Integer, nullable=False),
    sa.Column('level', sa.Integer, nullable=False)
)

ancestor_fk = ForeignKeyConstraint([comments_tree.c.ancestor_id], [comments.c.id])
descendant_fk = ForeignKeyConstraint([comments_tree.c.descendant_id], [comments.c.id])


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    ancestor_fk.create()
    descendant_fk.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    ancestor_fk.drop()
    descendant_fk.drop()
