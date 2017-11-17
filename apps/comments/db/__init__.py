from importlib import import_module

comments_module = import_module('apps.comments.db.versions.001_add_comments')

comments = getattr(comments_module, 'comments')
