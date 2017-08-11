import logging

import sqlalchemy as sa

logger = logging.getLogger(__name__)

__all__ = [
    "catalogue", "documents", "setup_models", "serialize_document",
    "serialize_child"
]

meta = sa.MetaData()

documents = sa.Table(
    "documents", meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("text", sa.UnicodeText)
)

catalogue = sa.Table(
    "catalogue", meta,
    sa.Column("parent_id", sa.Integer, nullable=True),
    sa.Column("child_id", sa.Integer),
    sa.UniqueConstraint("parent_id", "child_id")
)


def serialize_document(document, compact=True):
    if compact:
        return document[0]
    return {
        "id": document[0],
        "text": document[1],
    }


async def setup_models(app):
    async with app["db"].acquire() as cnx:
        async with cnx.begin():
            query = """create table if not exists {table} (
            {id} serial primary key,
            {text} {text_type},
            tsv tsvector)
            """.format(
                table=documents.name, id=documents.columns.id.name,
                text=documents.columns.text.name,
                text_type=documents.columns.text.type
            )
            logger.debug(query)
            await cnx.execute(query)

            query = """create table if not exists {table} (
            {parent_id} {parent_id_type} null,
            {child_id} {child_id_type} references {documents_table} ({documents_id}),
            constraint UC_{table} unique ({parent_id}, {child_id}))
            """.format(
                table=catalogue.name,
                parent_id=catalogue.columns.parent_id.name,
                parent_id_type=catalogue.columns.parent_id.type,
                child_id=catalogue.columns.child_id.name,
                child_id_type=catalogue.columns.child_id.type,
                documents_table=documents.name,
                documents_id=documents.columns.id.name
            )
            logger.debug(query)
            await cnx.execute(query)

            query = """drop trigger if exists {table}_tsv_vector_update
            on {table}
            """.format(table=documents.name, text=documents.columns.text.name)
            logger.debug(query)
            await cnx.execute(query)

            query = """create trigger {table}_tsv_vector_update
            before insert or update on {table}
            for each row execute procedure
            tsvector_update_trigger(tsv, 'pg_catalog.english', {text})
            """.format(
                table=documents.name, text=documents.columns.text.name
            )
            logger.debug(query)
            await cnx.execute(query)
