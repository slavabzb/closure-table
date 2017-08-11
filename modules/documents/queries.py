from .models import catalogue, documents, serialize_document

__all__ = ["DocumentNotFound", "documents_create", "documents_fetch"]


class DocumentNotFound(Exception):
    "Requested document in database was not found"


async def documents_create(cnx, text, parent_id=None):
    document_id = await cnx.scalar(documents.insert().values(text=text))
    await cnx.execute(catalogue.insert().values(
        parent_id=parent_id, child_id=document_id
    ))
    return document_id

async def documents_fetch(cnx, document_id=None):
    query = documents.select()
    if document_id:
        query = query.where(documents.c.id==document_id)
    return [serialize_document(doc) for doc in await cnx.execute(query)]
