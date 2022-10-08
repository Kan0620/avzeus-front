from typing import Callable
from collections import defaultdict
import os
import csv
import glob

from fastapi import FastAPI
import pandas as pd
import tweepy


def _startup_model(app: FastAPI) -> None:
    URL = os.environ["URL"]
    with open("app/static/js/raw_cut.js", "r") as raw_cut:
        print(URL)
        code = raw_cut.read()
        with open("app/static/js/cut.js", "w") as cut:
            code = code.replace("CUT_URL", URL + "cut")
            cut.write(code)
    with open("app/static/js/raw_predict.js", "r") as raw_cut:
        ORIGIN = os.environ["ORIGIN"]
        code = raw_cut.read()
        with open("app/static/js/predict.js", "w") as cut:
            code = code.replace("PREDICT_URL", URL + "predict").replace("ORIGIN", ORIGIN)
            cut.write(code)
    app.state.profile_df = pd.read_csv(os.environ["DATA_URL"]+"1000actress_with_profile_https.csv")
    app.state.profile_df = app.state.profile_df.sort_values(by="rubys")
    app.state.profile_df["hiragana"] = app.state.profile_df["rubys"].map(lambda x: x[0])
    app.state.rec_actress_id = 1044864
    app.state.sample_img_df = pd.read_csv(os.environ["DATA_URL"]+"id_with_sampleImageURL_https.csv")
    app.state.hiragana_list = [
        ["あ", "い", "う", "え", "お"],
        ["か", "き", "く", "け", "こ"],
        ["さ", "し", "す", "せ", "そ"],
        ["た", "ち", "つ", "て", "と"],
        ["な", "に", "ぬ", "ね", "の"],
        ["は", "ひ", "ふ", "へ", "ほ"],
        ["ま", "み", "む", "め", "も"],
        ["や", "ゆ", "よ"],
        ["ら", "り", "る", "れ", "ろ"],
        ["わ", "を"]
    ]
    app.state.actress_dict = defaultdict(lambda: [])
    for hiragana_gyou in app.state.hiragana_list:
        for hiragana in hiragana_gyou :
            for img_url, id, name in app.state.profile_df.loc[app.state.profile_df["hiragana"]==hiragana, ["imageURL", "id", "name"]].values:
                app.state.actress_dict[hiragana].append([img_url, id, name])
    app.state.twitter_client = tweepy.Client(
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
        )
    auth = tweepy.OAuth1UserHandler(
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
        )
    app.state.twitter_api  = tweepy.API(auth)



def _shutdown_model(app: FastAPI) -> None:
    os.remove("app/js/static/cut.js")
    os.remove("app/js/static/predict.js")
    
    

def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        _startup_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        _shutdown_model(app)

    return shutdown
