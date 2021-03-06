import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import index, img_rec, mov_rec, img_rec_result
from app.settings.settings import api_info, tags_info

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

if __name__ == '__main__':
    # コンソールで [$ uvicorn run:app --reload]でも可
    uvicorn.run(app=app)