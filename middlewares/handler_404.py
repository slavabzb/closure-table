from aiohttp.web import Response


async def handle_404(request, response):
    return Response(status=404, text="Not Found :(")
