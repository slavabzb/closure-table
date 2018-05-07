import hashlib
from datetime import datetime, timedelta

import jwt
from aiohttp import web
from closure_table.auth.db.queries import user_get
from closure_table.settings import JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS, JWT_SECRET


async def user_login_view(request):
    params = await request.json()
    email = params.get('email')
    password = params.get('password')
    async with request.app['db'].acquire() as conn:
        user = await user_get(conn, email)
    m = hashlib.sha512()
    m.update(str(password).encode())
    m.update(str(user.get('id')).encode())
    if email != user.get('email') or m.hexdigest() != user.get('password'):
        return web.json_response(status=400, data={
            'error': 'Incorrect email or password'
        })
    expired = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    payload = {
        'email': user['email'],
        'exp': expired
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return web.json_response({
        'token': jwt_token.decode(),
        'expired': expired.strftime('%c'),
    })
