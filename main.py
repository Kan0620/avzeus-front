import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import index, img_rec, mov_rec
from settings.settings import api_info, tags_info

app = FastAPI(
    title=api_info["title"],
    description=api_info["description"],
    version=api_info["version"],
    openapi_tags=tags_info
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(index.router, tags=["index"])
app.include_router(img_rec.router, tags=["index"])
app.include_router(mov_rec.router, tags=["index"])

if __name__ == '__main__':
    # コンソールで [$ uvicorn run:app --reload]でも可
    uvicorn.run(app=app)