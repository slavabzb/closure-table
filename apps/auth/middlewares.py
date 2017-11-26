import jwt
from aiohttp import web
from settings import JWT_SECRET, JWT_ALGORITHM
from .db.queries import user_get

async def auth_middleware(app, handler):
    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('X-Auth-Token')
        if jwt_token:
            try:
                payload = jwt.decode(
                    jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
                )
            except jwt.DecodeError:
                return web.json_response(status=400, data={
                    'error': 'Auth token is invalid'
                })
            except jwt.ExpiredSignatureError:
                return web.json_response(status=400, data={
                    'error': 'Auth token is expired'
                })

            async with request.app['db'].acquire() as conn:
                request.user = await user_get(conn, payload['email'])

        return await handler(request)
    return middleware
