from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="static")

@router.get("/img-rec-result/{img:path}", response_class=HTMLResponse)
async def img_rec_result(img: str, request: Request):
    return templates.TemplateResponse(
        "img-rec-result.html",
        {
            "request": request,
            }
    )