from aiohttp import web
from .queries import document_create

__all__ = ["document_create_view"]


async def document_create_view(request):
    """
    Description end-point
    ---
    tags:
    - Documents
    summary: Create document
    description: This can only be done by the logged in user.
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
    "201":
      description: successful operation
    """
    async with request.app["db"].acquire() as cnx:
        params = await request.json()
        text = params["text"]
        parent_id = params["parent_id"]
        # document_create(cnx, text, parent_id)
        return web.json_response({
            "status": "success",
            "text": text,
            "parent_id": parent_id
        })
