from apps.comments.views import create_view

ENDPOINT = '/comments'


def setup_routes(app):
    docs = app.router.add_resource(ENDPOINT)
    docs.add_route('POST', create_view)
