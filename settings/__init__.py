import os

DEBUG = os.environ.get("DEBUG", None)

if DEBUG:
    from .dev import *
else:
    from .prod import *
