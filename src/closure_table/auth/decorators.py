from functools import wraps

from aiohttp.web import json_response


def login_required(view):
    @wraps(view)
    def wrapper(request):
        if not request.user:
            return json_response(status=403, data={
                'error': 'Authorization required'
            })
        return view(request)

    return wrapper
