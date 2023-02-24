from config import ALLOW_PATH, CONFIG
from utils import check, error_403, error_404

from os import listdir
from os.path import abspath, basename, isdir, isfile, join
from typing import Optional
from urllib.parse import quote

from aiofiles import open as aopen
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import Config, Server

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index(path: Optional[str] = None):
    async with aopen("index.html") as index_file:
        content = await index_file.read()
    path = ALLOW_PATH.root if path in ("/", None) else path

    check_res = check(path)
    if check_res is False:
        return await error_403()
    elif check_res is None:
        return await error_404()

    path = abspath(path)
    if isdir(path):
        upper_path = abspath(join(path, ".."))
        add_list = ["<div><a href=\"/?path={}\">..</a></div>".format(upper_path.replace("\\", "/"))] if check(upper_path) else []
        content = content.replace("$LOCATION", path)
        content = content.replace(
            "$LIST",
            "\n".join(
                add_list + 
                [
                    "<div><a href=\"/?path={}\">{}</a> - {}</div>".format(
                        quote(filepath.replace('\\', '/')), basename(filepath), "dir" if isdir(filepath) else "file")
                    for filepath in filter(check, map(lambda target: abspath(join(path, target)), listdir(path)))
                ]
            )
        )
        return HTMLResponse(content)
    if isfile(path):
        return FileResponse(path, filename=basename(path) or "Unknow", content_disposition_type="inline")
    return await error_404()


@app.exception_handler(403)
async def access_denied(requests, exc):
    return await error_403()


@app.exception_handler(404)
async def not_found(requests, exc):
    return await error_404()


def run():
    config = Config(app, host=CONFIG.host, port=CONFIG.port)
    server = Server(config=config)
    server.run()


if __name__ == "__main__":
    run()
