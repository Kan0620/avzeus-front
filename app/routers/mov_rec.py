import os
import re

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup as bs

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
    if saw_ids == "init":
        saw_ids = ""
    else:
        saw_ids += "-"
    return templates.TemplateResponse(
        "html/mov-rec.html",
        
        {
            "request": request,
            "ORIGIN": os.environ["ORIGIN"],
            "saw_ids": saw_ids,
            "mov_id": mov_id,
            "mov_url": f"https://cc3001.dmm.co.jp/litevideo/freepv/{mov_id[0]}/{mov_id[:3]}/{mov_id}/{mov_id}_dmb_w.mp4",
            "mov_title": r.json()["result"]["movie"]["title"],
            "affiliateURL": r.json()["result"]["movie"]["affiliateURL"],
            "thumbnails": thumbnails
                
            }
    )