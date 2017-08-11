from aiohttp import web
from .queries import documents_create, documents_fetch

__all__ = ["documents_create_view", "documents_view", "document_view"]


def make_response(data, message=None):
    return web.json_response({"message": message, "documents": data})


async def documents_view(request):
    """
    ---
    tags:
    - Documents
    summary: Fetch documents.
    description: Fetch documents.
    produces:
    - application/json
    responses:
    "200":
      description: successful operation
    """
    async with request.app["db"].acquire() as cnx:
        documents = await documents_fetch(cnx)
        if documents:
            message = "records found ({})".format(len(documents))
        else:
            message = "records not found"
        return make_response(documents, message=message)


async def documents_create_view(request):
    """
    ---
    tags:
    - Documents
    summary: Create new document.
    description: Create new document. To create new root document send
                 parent_id=0.
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      description: Created document
      required: true
      schema:
        type: object
        properties:
          text:
            type: string
            required: true
          parent_id:
            format: int32
            type: integer
    responses:
    "200":
      description: successful operation
    """
    async with request.app["db"].acquire() as cnx:
        params = await request.json()
        text = params["text"]
        parent_id = params["parent_id"]
        document_id = await documents_create(cnx, text, parent_id)
        return make_response(message="records created", data={
            "id": document_id
        })


async def document_view(request):
    """
    ---
    tags:
    - Documents
    summary: Fetch document.
    description: Fetch document.
    produces:
    - application/json
    parameters:
    - in: path
      name: id
      description: Document ID
      required: true
      type: integer
    responses:
    "200":
      description: successful operation
    """
    async with request.app["db"].acquire() as cnx:
        document_id = request.match_info["id"]
        documents = await documents_fetch(cnx, document_id)
        if documents:
            message = "records found ({})".format(len(documents))
        else:
            message = "records not found"
        return make_response(documents, message=message)
