from apps.comments.views import get_tree_view, create_view

ENDPOINT = '/comments'


def setup_routes(app):
    comment = app.router.add_resource(ENDPOINT + '/{id}')
    comment.add_route('GET', get_tree_view)

    comment_collection = app.router.add_resource(ENDPOINT)
    comment_collection.add_route('POST', create_view)
