import sqlalchemy as sa

from .models import catalogue, documents, serialize_document

__all__ = [
    "documents_create", "documents_search", "documents_update",
    "documents_children", "documents_detail"
]


async def documents_create(cnx, text, parent_id=None):
    document_id = await cnx.scalar(documents.insert().values(text=text))
    await cnx.execute(catalogue.insert().values(
        parent_id=parent_id, child_id=document_id
    ))
    return document_id


async def documents_search(cnx, text):
    query = documents.select().where(documents.c.text.match(text))
    return [
        serialize_document(document, compact=True)
        for document in await cnx.execute(query)
    ]


async def documents_detail(cnx, document_id):
    query = documents.select().where(documents.c.id == document_id)
    return [
        serialize_document(document, compact=False)
        for document in await cnx.execute(query)
    ]


async def documents_children(cnx, document_id):
    join = sa.join(documents, catalogue,
                   documents.c.id == catalogue.c.parent_id)
    query = sa.select([catalogue.c.child_id]) \
        .select_from(join) \
        .where(documents.c.id == document_id)
    return [row[0] for row in await cnx.execute(query)]


async def documents_update(cnx, document_id, parent_id, text):
    async with cnx.begin():
        await cnx.execute(
            catalogue.delete(catalogue.c.child_id == document_id)
        )
        await cnx.execute(
            catalogue.insert().values(parent_id=parent_id,
                                      child_id=document_id)
        )
        await cnx.execute(
            documents.update()
                .where(documents.c.id == document_id)
                .values(text=text)
        )
