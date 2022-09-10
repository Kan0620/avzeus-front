import os
import random

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/static")

@router.get("/article/{id}", response_class=HTMLResponse)
async def mov_rec(id: int, request: Request, lang: str = "ja"):
    if lang in ["ja", "en", "zh"]:
        df = request.app.state.profile_df
        img_df = request.app.state.sample_img_df
        en_keys = ["name", "bust", "cup", "waist", "hip", "height", "birthday", "blood_type", "hobby", "prefectures"]
        ja_keys = ["名前", "バスト", "カップ", "ウエスト", "ヒップ", "身長", "誕生日", "血液型", "趣味", "出身地"]
        profiles = []
        for en_key in en_keys:
            profiles.append(df.loc[df["id"]==id, en_key].tolist()[0])
        sample_img_urls = img_df.loc[img_df["id"]==id, "sampleImageURL"].tolist()
        sample_img_urls = random.sample(sample_img_urls, len(sample_img_urls))
        if len(sample_img_urls) > 50:
            sample_img_urls = sample_img_urls[:50]
        mov_cids = list(map(lambda x: x.split("/")[-2], sample_img_urls))
        return templates.TemplateResponse(
            f"html/{lang}/article.html",
            {
                "request": request,
                "ORIGIN": os.environ["ORIGIN"],
                "lang": lang,
                "actress_id": id,
                "actress_name": df.loc[df["id"]==id, "name"].tolist()[0],
                "actress_link": df.loc[df["id"]==id, "affiliateURL"].tolist()[0],
                "actress_img": df.loc[df["id"]==id, "imageURL"].tolist()[0],
                "profiles": zip(ja_keys, profiles),
                "sample_img_urls": zip(sample_img_urls, mov_cids)
                }
        )
    