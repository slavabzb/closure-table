from importlib import import_module

documents_module = import_module('apps.documents.db.versions.001_add_documents')

documents = getattr(documents_module, 'documents')
