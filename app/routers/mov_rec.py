import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import requests

router = APIRouter()
templates = Jinja2Templates(directory="app/static")

@router.get("/mov-rec/{saw_ids}", response_class=HTMLResponse)
async def mov_rec(saw_ids: str, request: Request):
    if os.environ["APP_ENV"] == "local":
        post_url = "http://host.docker.internal:80/api/v1/mov-rec"
    else:
        post_url = os.environ["URL"] + "mov-rec"
    r = requests.post(post_url, json={"input_text": saw_ids})
    mov_id = r.json()["result"]["movie"]["content_id"]
    thumbnails = [[item["content_id"], item["title"], item["imageURL"]] for item in r.json()["result"]["thumbnails"]]
    return templates.TemplateResponse(
        "mov-rec.html",
        {
            "request": request,
            "ORIGIN": os.environ["ORIGIN"],
            "mov_url": "https://cc3001.dmm.co.jp/litevideo/freepv/i/ipx/ipx00344/ipx00344_dmb_w.mp4",
            "mov_title": r.json()["result"]["movie"]["title"],
            "mov_id": r.json()["result"]["movie"]["content_id"],
            "thumbnails": thumbnails
                
            }
    )