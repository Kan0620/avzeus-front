import os
import random

import numpy as np
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

router = APIRouter()



class GetRequest(BaseModel):
    password: str = Field(..., title="password", example="example")
    id: int = Field(..., title="id", example=-1)
class ReturnResponse(BaseModel):
    result: str = Field(..., title="result", description="Response", example="succeed")

@router.post("/regularly-actress-tweet", response_model=ReturnResponse)
async def regularly_actress_tweet(request: Request, payload: GetRequest):
    if payload.password == os.environ["TWEET_PASSWORD"]:
        
        df = request.app.state.profile_df
        if payload.id == -1:
            id = random.choice(list(set(df["id"].tolist())-set([request.app.state.rec_actress_id])))
        else:
            if payload.id in set(df["id"].tolist()):
                id = payload.id
            else:
                return ReturnResponse(result="invalid id")
        rec_actress_name = df.loc[df["id"]==id, "name"].tolist()[0]
        text = f"""【AV女優紹介】\n\nみんな #{rec_actress_name} さんを知っとるかの？\nプロフィールと画像ををまとめたからぜひ見てくれよの！\nhttps://www.av-zeus.com/article/{id}\n\n#{rec_actress_name}\n#FANZA\n#AV\n#AV女優\n#AVゼウス"""
        request.app.state.twitter_client.create_tweet(text=text)
        return ReturnResponse(result=text)
        
    else:
        return ReturnResponse(result="invalid password")
        