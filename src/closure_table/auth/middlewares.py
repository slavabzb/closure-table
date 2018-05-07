import jwt
from aiohttp.web import json_response
from closure_table.auth.db.queries import user_get
from closure_table.settings import JWT_ALGORITHM, JWT_SECRET


def setup_middlewares(app):
    app.middlewares.append(auth_middleware)


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
                return json_response(status=400, data={
                    'error': 'Auth token is invalid'
                })
            except jwt.ExpiredSignatureError:
                return json_response(status=400, data={
                    'error': 'Auth token is expired'
                })

            async with request.app['db'].acquire() as conn:
                request.user = await user_get(conn, payload['email'])

        return await handler(request)

    return middleware
