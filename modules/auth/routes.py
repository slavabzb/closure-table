from .views import login_view, logout_view

__all__ = ["setup_routes"]

BASE_URL = "/users"


def setup_routes(app):
    app.router.add_post(BASE_URL + "/login", login_view)
    app.router.add_get(BASE_URL + "/logout", logout_view, allow_head=False)
