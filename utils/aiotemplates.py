from aiofiles import open as aopen
from fastapi.responses import HTMLResponse


async def error_404() -> HTMLResponse:
    async with aopen("404.html", mode="rb") as html_file:
        return HTMLResponse(await html_file.read(), 404)


async def error_403() -> HTMLResponse:
    async with aopen("403.html", mode="rb") as html_file:
        return HTMLResponse(await html_file.read(), 403)
