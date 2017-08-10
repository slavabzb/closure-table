from .views import documents_create_view, documents_fetch_view

__all__ = ["setup_routes"]


def setup_routes(app):
    app.router.add_get("/documents", documents_fetch_view, allow_head=False)
    app.router.add_post("/documents", documents_create_view)
