import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/static")

@router.get("/img-rec-result/{result}", response_class=HTMLResponse)
async def img_rec_result(result: str, request: Request):
    result_ids = result.split("-")
    names = []
    imageURLs = []
    affiliateURLs = []
    for result_id in result_ids:
        index = request.app.state.ids.index(result_id)
        names .append(request.app.state.names[index])
        imageURLs.append(request.app.state.imageURLs[index].replace("http:", "https:"))
        affiliateURLs.append(request.app.state.affiliateURLs[index])
    return templates.TemplateResponse(
        "img-rec-result.html",
        {
            "request": request,
            "ORIGIN": os.environ["ORIGIN"],
            "data": zip(names, result_ids, imageURLs, affiliateURLs)
            }
    )
    