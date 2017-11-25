from .views import user_login_view

ENDPOINT = '/auth'


def setup_routes(app):
    app.router.add_route('POST', ENDPOINT + '/login', user_login_view)
