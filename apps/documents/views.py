import os

from aiohttp import web
from aiohttp_swagger import swagger_path

from .db.tables import documents


@swagger_path(os.path.join('apps', 'documents', 'docs', 'create_view.yaml'))
async def create_view(request):
    params = await request.json()
    parent_id = params.get('parent_id')
    text = params.get('text')
    if not text:
        return web.json_response(status=400, data={
            'error': 'text cannot be empty'
        })
    async with request.app['db'].acquire() as conn:
        document_id = await conn.scalar(documents.insert().values(text=text))
        return web.json_response({
            'id': document_id
        })
