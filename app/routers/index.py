import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/static")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, lang: str = "ja"):
    if lang in ["ja", "en", "zh"]:
        return templates.TemplateResponse(
            f"html/{lang}/index.html",
            {
                "request": request,
                "ORIGIN": os.environ["ORIGIN"],
                "lang": lang
                }
        )
    