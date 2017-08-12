import functools

from aiohttp import web
from aiohttp_security import remember, forget, permits

from .policy import check_credentials

__all__ = ["login_view", "logout_view"]


def require(permission):
    def wrapper(f):
        @functools.wraps(f)
        async def wrapped(request):
            has_perm = await permits(request, permission)
            if not has_perm:
                return web.json_response(status=403, data={
                    "status": "user has no permission"
                })
            return await f(request)

        return wrapped

    return wrapper


async def login_view(request):
    """
    ---
    tags:
    - Users
    summary: User login.
    description: Login user.
    produces:
    - application/json
    parameters:
    - in: body
      name: body
      description: User credentials.
      required: true
      schema:
        type: object
        properties:
          username:
            type: string
            required: true
          password:
            type: string
            required: true
    """
    response = web.json_response({"status": "logged in"})
    params = await request.json()
    username = params["username"]
    password = params["password"]
    db_engine = request.app["db"]
    if await check_credentials(db_engine, username, password):
        await remember(request, response, username)
        return response
    return web.json_response({"status": "unathorized"}, status=401)


@require("public")
async def logout_view(request):
    """
    ---
    tags:
    - Users
    summary: User logout.
    description: Logout user.
    produces:
    - application/json
    """
    response = web.json_response({"status": "logged out"})
    await forget(request, response)
    return response
