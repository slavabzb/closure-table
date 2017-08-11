import logging
from aiohttp.web import HTTPException, json_response

from .handle_500 import handle_500
from .handler_404 import handle_404


def error_handlers(overrides):
    async def middleware(app, handler):
        async def middleware_handler(request):
            try:
                response = await handler(request)
                override = overrides.get(response.status)
                if override is None:
                    return response
                else:
                    return await override(request, response)
            except HTTPException as ex:
                override = overrides.get(ex.status)
                if override is None:
                    raise
                else:
                    return await override(request, ex)
            except Exception as ex:
                logger = logging.getLogger(__name__)
                logger.exception(ex)
                return json_response({"error": "invalid request"}, status=400)

        return middleware_handler

    return middleware


def setup_middlewares(app):
    error_middleware = error_handlers({404: handle_404,
                                       500: handle_500})
    app.middlewares.append(error_middleware)
