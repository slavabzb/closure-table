import hashlib
from aiohttp import web

from .db.queries import user_get


async def user_login_view(request):
    params = await request.json()
    email = params.get('email')
    password = params.get('password')
    async with request.app['db'].acquire() as conn:
        user = await user_get(conn, email)
        m = hashlib.sha512()
        m.update(str(password).encode())
        m.update(str(user.get('id')).encode())
        if email == user.get('email') and m.hexdigest() == user.get('password'):
            return web.json_response({'token': 'token'})
    return web.json_response(status=401)
