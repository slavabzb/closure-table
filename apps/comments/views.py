from aiohttp import web

from apps.comments.db import comments


async def create_view(request):
    params = await request.json()
    parent_id = params.get('parent_id')
    content = params.get('content')
    if not content:
        return web.json_response(status=400, data={
            'error': 'content cannot be empty'
        })
    async with request.app['db'].acquire() as conn:
        comment_id = await conn.scalar(comments.insert().values(content=content))
        return web.json_response({
            'id': comment_id
        })
