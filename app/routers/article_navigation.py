import os
import random

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/static")

@router.get("/article-navigation", response_class=HTMLResponse)
async def index(request: Request, lang: str = "ja"):
    if lang in ["ja", "en", "zh"]:
        df = request.app.state.profile_df
        id = request.app.state.weekly_actress_id
        random_actress_id = random.sample(df["id"].tolist(), 1)[0]
        return templates.TemplateResponse(
            f"html/{lang}/article-navigation.html",
            {
                "request": request,
                "ORIGIN": os.environ["ORIGIN"],
                "lang": lang,
                "weekly_actress_id": id,
                "weekly_actress_name": df.loc[df["id"]==id, "name"].tolist()[0],
                "weekly_actress_link": df.loc[df["id"]==id, "affiliateURL"].tolist()[0],
                "weekly_actress_img": df.loc[df["id"]==id, "imageURL"].tolist()[0],
                "random_actress_id": random_actress_id,
                "hiragana_list": request.app.state.hiragana_list,
                "actress_dict": request.app.state.actress_dict
                }
        )
    