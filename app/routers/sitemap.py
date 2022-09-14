import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/static")

@router.get("/sitemap", response_class=HTMLResponse)
async def sitemap(request: Request):
    return templates.TemplateResponse(
        "sitemap/sitemap.xml",
        {
            "request": request,
            }
    )
    