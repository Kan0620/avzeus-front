import os
import random

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

@router.post("/change-rec-actress-and-tweet", response_model=ReturnResponse)
async def change_rec_actress_and_tweet(request: Request, payload: GetRequest):
    if payload.password == os.environ["TWEET_PASSWORD"]:
        df = request.app.state.profile_df
        if payload.id == -1:
            request.app.state.rec_actress_id = random.choice(list(set(df["id"].tolist())-set([request.app.state.rec_actress_id])))
        else:
            if payload.id in set(df["id"].tolist()):
                request.app.state.rec_actress_id = payload.id
            else:
                return ReturnResponse(result="invalid id")
                
        #request.app.state.twitter_client.create_tweet(text="test")
        return ReturnResponse(result="succeed")
    else:
        return ReturnResponse(result="invalid password")
        