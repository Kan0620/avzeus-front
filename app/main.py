import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import index, img_rec, mov_rec, img_rec_result, article_navigation, article, regularly_tweet, sitemap
from app.settings.settings import api_info, tags_info
from app.core.event_handler import start_app_handler, stop_app_handler

app = FastAPI(
    title=api_info["title"],
    description=api_info["description"],
    version=api_info["version"],
    openapi_tags=tags_info
)
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

app.include_router(index.router, tags=["html"])
app.include_router(img_rec.router, tags=["html"])
app.include_router(img_rec_result.router, tags=["html"])
app.include_router(mov_rec.router, tags=["html"])
app.include_router(article_navigation.router, tags=["html"])
app.include_router(article.router, tags=["html"])
app.include_router(sitemap.router, tags=["html"])
app.include_router(regularly_tweet.router, tags=["html"])

app.add_event_handler("startup", start_app_handler(app))
app.add_event_handler("shutdown", stop_app_handler(app))
