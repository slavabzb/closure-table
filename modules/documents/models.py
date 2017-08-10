import sqlalchemy as sa

__all__ = ["documents"]

meta = sa.MetaData()

documents = sa.Table(
    "documents", meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("parent_id", sa.Integer, nullable=True),
    sa.Column("text", sa.String)
)
