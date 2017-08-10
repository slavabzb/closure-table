from .views import document_create_view

__all__ = ["setup_routes"]


def setup_routes(app):
    app.router.add_post("/documents", document_create_view)
