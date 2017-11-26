from functools import wraps

from aiohttp import web


def login_required(view):
    @wraps(view)
    def wrapper(request):
        if not request.user:
            return web.json_response(status=403, data={
                'error': 'Authorization required'
            })
        return view(request)

    return wrapper
