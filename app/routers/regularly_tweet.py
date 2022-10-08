import os
import random
import base64
from io import BytesIO

import numpy as np
from PIL import Image
import requests
from fastapi import APIRouter
from fastapi.requests import Request
from pydantic import BaseModel, Field

from .. import main


router = APIRouter()



class GetRequest(BaseModel):
    password: str = Field(..., title="password", example="example")
    tweet_type: str = Field(..., title="tweet_type", example="random")
    id: int = Field(..., title="id", example=-1)
class ReturnResponse(BaseModel):
    result: str = Field(..., title="result", description="Response", example="succeed")

@router.post("/regularly-tweet", response_model=ReturnResponse)
async def regularly_tweet(request: Request, payload: GetRequest):
    if payload.password == os.environ["TWEET_PASSWORD"]:
        tweet_types = ["rec_actress", "img_rec", "mov_rec", "article_navigation"]
        if payload.tweet_type in tweet_types:
            tweet_type = payload.tweet_type
        else:
            tweet_type = np.random.choice(tweet_types, p=[0.7, 0.1, 0.1, 0.1])
        
        if tweet_type == "rec_actress":
            df = request.app.state.profile_df
            if payload.id == -1:
                main.app.state.rec_actress_id = random.choice(list(set(df["id"].tolist())-set([request.app.state.rec_actress_id])))
            else:
                if payload.id in set(df["id"].tolist()):
                    main.app.state.rec_actress_id = payload.id
                else:
                    return ReturnResponse(result="invalid id")
            rec_actress_name = df.loc[df["id"]==main.app.state.rec_actress_id, "name"].tolist()[0]
            text = f"""【今日のおすすめAV女優】\n\n今日のおすすめAV女優は #{rec_actress_name} じゃ！\nプロフィールと画像ををまとめたからぜひ見てくれよの！\nhttps://www.av-zeus.com/article/{request.app.state.rec_actress_id}\n\n#{rec_actress_name}\n#FANZA\n#AV\n#AV女優\n#AVゼウス"""
            request.app.state.twitter_client.create_tweet(text=text)
            print("rec_actress", len(text))
            
            img_df = request.app.state.sample_img_df
            img_urls = img_df.loc[img_df["id"]==request.app.state.rec_actress_id, "sampleImageURL"].tolist()
            if 5 <= len(img_urls):
                img_urls = random.sample(img_urls, 4)
            media_ids = []
            for img_i, img_url in enumerate(img_urls):
                response = requests.get(img_url)
                image = response.content
                img_name = f"app/static/img/{img_i}.png"
                with open(img_name, "wb") as img_file:
                    img_file.write(image)
                media = request.app.state.twitter_api.media_upload(img_name)
                media_ids.append(media.media_id)


            text = f"""【今日のおすすめAV女優 画像】\n\n今日のおすすめAV女優は #{rec_actress_name} の画像じゃ！\nこのリンクから他の画像も見れるぞい！\nhttps://www.av-zeus.com/article/{request.app.state.rec_actress_id}\n\n#{rec_actress_name}\n#FANZA\n#AV\n#AV女優\n#AVゼウス"""
            request.app.state.twitter_api.update_status(status=text, media_ids=media_ids)
        
            
            
            return ReturnResponse(result=request.app.state.rec_actress_id)
        elif tweet_type == "img_rec":
            text = f"""【AVゼウス 画像レコメンドモード】\n\n今日はAVゼウスの画像レコメンドモードを紹介するぞい！\nこれページはお主のお好みの女の子の画像をアップすると1000人のAV女優から顔が似ている子をわしがおすすめする機能じゃ！\nhttps://www.av-zeus.com/img-rec/\n\n#FANZA\n#AV\n#AV女優\n#AVゼウス"""
            print("img_rec", len(text))
            request.app.state.twitter_client.create_tweet(text=text)
            return ReturnResponse(result=tweet_type)
        elif tweet_type == "mov_rec":
            text = f"""【AVゼウス 動画レコメンドモード】\n\n今日はAVゼウスの動画レコメンドモードを紹介するぞい！\nこのページはFANZAのAVを見やすくまとめたものじゃ、そこからFANZAのページに飛べるぞい！\nhttps://www.av-zeus.com/mov-rec/\n\n#FANZA\n#AV\n#AV女優\n#AVゼウス"""
            print("mov_rec", len(text))
            request.app.state.twitter_client.create_tweet(text=text)
            return ReturnResponse(result=tweet_type)
        elif tweet_type == "article":
            text = f"""【AVゼウス 記事閲覧モード】\n\n今日はAVゼウスの記事閲覧モードを紹介するぞい！\nこのページには1000人のAV女優のプロフィールと画像をまとめた記事へのリンクがあるぞい！お主のAV女優が見つかるはずじゃ！\nhttps://www.av-zeus.com/article-navigation/\n\n#FANZA\n#AV\n#AV女優\n#AVゼウス"""
            request.app.state.twitter_client.create_tweet(text=text)
            return ReturnResponse(result=tweet_type)
        else:
            return ReturnResponse(result="invalid tweet_type")
            
    else:
        return ReturnResponse(result="invalid password")
        