from importlib import import_module

mod = import_module('db.versions.001_add_document_table')

document = getattr(mod, 'document')
