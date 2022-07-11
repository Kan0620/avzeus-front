from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="static")

@router.get("/mov-rec", response_class=HTMLResponse)
async def mov_rec(request: Request):
    return templates.TemplateResponse(
        "mov-rec.html",
        {
            "request": request,
            }
    )