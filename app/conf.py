import settings
from utils import load_conf


async def load_app_conf(app):
    app["config"] = load_conf(settings.DB_CONF)
