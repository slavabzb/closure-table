from aiohttp import web
from .queries import documents_create, documents_fetch

__all__ = ["documents_create_view", "documents_fetch_view"]


async def documents_fetch_view(request):
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
        return web.json_response({"documents": documents})


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
        await documents_create(cnx, text, parent_id)
        return web.Response()
