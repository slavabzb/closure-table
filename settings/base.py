import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_CONF = os.environ.get("DB_CONF")
APP_CONF = os.environ.get("APP_CONF")

DEBUG = bool(os.environ.get("DEBUG", "False"))

if DEBUG:
    from .dev import *
else:
    from .prod import *
