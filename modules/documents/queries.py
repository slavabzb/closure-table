from .models import documents

__all__ = ["DocumentNotFound", "document_create"]


class DocumentNotFound(Exception):
    "Requested document in database was not found"


async def document_create(cnx, text, parent_id=None):
    result = await cnx.execute(
        documents.insert().values(text=text, parent_id=parent_id)
    )
    x = 1
