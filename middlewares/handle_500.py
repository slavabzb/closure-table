from aiohttp.web import Response


async def handle_500(request, response):
    return Response(status=500, text="Server is drinking coffee :(")
