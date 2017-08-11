from .views import documents_create_view, documents_view, document_view

__all__ = ["setup_routes"]

BASE_URL = "/documents"


def setup_routes(app):
    documents = app.router.add_resource(BASE_URL)
    documents.add_route("GET", documents_view)
    documents.add_route("POST", documents_create_view)

    document = app.router.add_resource(BASE_URL + "/{id}")
    document.add_route("GET", document_view)
