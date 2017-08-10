from .models import documents, serialize_document

__all__ = ["DocumentNotFound", "documents_create", "documents_fetch"]


class DocumentNotFound(Exception):
    "Requested document in database was not found"


async def documents_create(cnx, text, parent_id=None):
    await cnx.execute(
        documents.insert().values(
            text=text, parent_id=parent_id
        )
    )

async def documents_fetch(cnx):
    return [serialize_document(document) for document in await cnx.execute(
        documents.select()
    )]
