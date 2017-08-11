from .views import documents_create_view, documents_search_view,\
    documents_detail_view, documents_update_view, documents_children_view

__all__ = ["setup_routes"]

BASE_URL = "/documents"


def setup_routes(app):
    documents = app.router.add_resource(BASE_URL)
    documents.add_route("GET", documents_search_view)
    documents.add_route("POST", documents_create_view)

    document = app.router.add_resource(BASE_URL + "/{id}")
    document.add_route("GET", documents_detail_view)
    document.add_route("POST", documents_update_view)

    children = app.router.add_resource(BASE_URL + "/{id}/children")
    children.add_route("GET", documents_children_view)
