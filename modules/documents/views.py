from aiohttp import web

from .queries import documents_create, documents_search, documents_update, \
    documents_children, documents_detail

__all__ = [
    "documents_create_view", "documents_search_view", "documents_detail_view",
    "documents_update_view", "documents_children_view"
]


def make_response(values, message=None):
    if message is None:
        if values:
            message = "{} record(s) found".format(len(values))
        else:
            message = "no records found"
    return web.json_response({"message": message, "documents": values})


async def documents_children_view(request):
    """
    ---
    tags:
    - Documents
    summary: View subdocuments.
    description: View all the subdocuments of given document.
    produces:
    - application/json
    parameters:
    - in: path
      name: id
      description: Document ID
      required: true
      type: integer
    """
    async with request.app["db"].acquire() as cnx:
        document_id = request.match_info["id"]
        results = await documents_children(cnx, document_id)
        return make_response(results)


async def documents_search_view(request):
    """
    ---
    tags:
    - Documents
    summary: Search documents.
    description: Search documents by content.
    produces:
    - application/json
    parameters:
    - in: query
      name: text
      description: Query text.
      type: string
      required: false
    """
    async with request.app["db"].acquire() as cnx:
        params = request.query
        documents = await documents_search(cnx, text=params.get("text", None))
        return make_response(documents)


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
    """
    async with request.app["db"].acquire() as cnx:
        params = await request.json()
        text = params["text"]
        parent_id = params["parent_id"]
        document_id = await documents_create(cnx, text, parent_id)
        return make_response(message="records created", values={
            "id": document_id
        })


async def documents_detail_view(request):
    """
    ---
    tags:
    - Documents
    summary: View document details.
    description: View document details.
    produces:
    - application/json
    parameters:
    - in: path
      name: id
      description: Document ID
      required: true
      type: integer
    """
    async with request.app["db"].acquire() as cnx:
        document_id = request.match_info["id"]
        documents = await documents_detail(cnx, document_id)
        return make_response(documents)


async def documents_update_view(request):
    """
    ---
    tags:
    - Documents
    summary: Update document.
    description: Update existing document.
    produces:
    - application/json
    parameters:
    - in: path
      name: id
      description: Document ID
      required: true
      type: integer
    - in: body
      name: body
      description: The text of the document.
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
    """
    async with request.app["db"].acquire() as cnx:
        document_id = request.match_info["id"]
        params = await request.json()
        parent_id = params["parent_id"]
        text = params["text"]
        await documents_update(cnx, document_id, parent_id, text)
        return make_response(message="records updated", values=[document_id])
