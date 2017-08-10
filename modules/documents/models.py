import logging

import sqlalchemy as sa

logger = logging.getLogger(__name__)

__all__ = ["documents", "setup_models", "serialize_document"]

meta = sa.MetaData()

documents = sa.Table(
    "documents", meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("parent_id", sa.Integer, nullable=True),
    sa.Column("text", sa.UnicodeText)
)


def serialize_document(document):
    return {
        "id": document[0],
        "parent_id": document[1],
        "text": document[2],
    }


async def setup_models(app):
    # unable to use Document.metadata.create_all() here
    async with app["db"].acquire() as cnx:
        query = """create table if not exists {table} (
        {id} serial primary key,
        {parent_id} {parent_id_type} not null,
        {text} {text_type},
        tsv tsvector)""".format(
            table=documents.name, id=documents.columns.id.name,
            parent_id=documents.columns.parent_id.name,
            parent_id_type=documents.columns.parent_id.type,
            text=documents.columns.text.name,
            text_type=documents.columns.text.type
        )
        logger.debug(query)
        await cnx.execute(query)

        query = """drop trigger if exists {table}_tsv_vector_update
        on {table}""".format(table=documents.name,
                             text=documents.columns.text.name)
        logger.debug(query)
        await cnx.execute(query)

        query = """create trigger {table}_tsv_vector_update
        before insert or update on {table}
        for each row execute procedure
        tsvector_update_trigger(tsv, 'pg_catalog.english', {text})""".format(
            table=documents.name, text=documents.columns.text.name
        )
        logger.debug(query)
        await cnx.execute(query)
