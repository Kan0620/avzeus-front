import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/static")

@router.get("/img-rec", response_class=HTMLResponse)
async def img_rec(request: Request):
    return templates.TemplateResponse(
        "img-rec.html",
        {
            "request": request,
            "ORIGIN": os.environ["ORIGIN"],
            "cut_js_path": "cut.js",
            "predict_js_path": "predict.js"
            }
    )