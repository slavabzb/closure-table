from aiohttp import web
from closure_table.auth.decorators import login_required

from .db.queries import (
    comment_create,
    comment_update,
    comment_get_tree,
    comment_delete,
    comment_get,
    comment_search,
)


@login_required
async def comment_create_view(request):
    params = await request.json()
    parent_id = params.get('parent_id')
    content = params.get('content')
    if not content:
        return web.json_response(status=400)
    async with request.app['db'].acquire() as conn:
        comment_id = await comment_create(conn, content, parent_id)
        return web.json_response({'id': comment_id})


@login_required
async def comment_update_view(request):
    params = await request.json()
    content = params.get('content')
    if not content:
        return web.json_response(status=400)
    async with request.app['db'].acquire() as conn:
        count = await comment_update(conn, request.match_info['id'], content)
        return web.json_response({'updated': count})


@login_required
async def comment_delete_view(request):
    async with request.app['db'].acquire() as conn:
        count = await comment_delete(conn, request.match_info['id'])
        return web.json_response({'deleted': count})


async def comment_get_view(request):
    async with request.app['db'].acquire() as conn:
        comment_list = await comment_get(conn)
        return web.json_response({'comments': comment_list})


async def comment_get_tree_view(request):
    async with request.app['db'].acquire() as conn:
        tree = await comment_get_tree(conn, request.match_info['id'])
        if tree:
            return web.json_response(tree)
        return web.json_response(status=404)


async def comment_search_view(request):
    async with request.app['db'].acquire() as conn:
        comment_list = await comment_search(conn, request.match_info['text'])
        return web.json_response({'comments': comment_list})
