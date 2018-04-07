from closure_table.auth.views import user_login_view


def setup_routes(app):
    app.router.add_route('POST', '/auth/login', user_login_view)
