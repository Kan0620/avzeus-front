from typing import Callable
import os
import csv
import glob

from fastapi import FastAPI


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
    with open("app/data/actress_data.csv", "r") as f:
        reader = csv.reader(f)
        ids = []
        names = []
        imageURLs = []
        affiliateURLs = []
        for id, name, imageURL, affiliateURL in reader:
            ids.append(id)
            names.append(name)
            imageURLs.append(imageURL)
            affiliateURLs.append(affiliateURL)
        app.state.ids = ids
        app.state.names = names
        app.state.imageURLs = imageURLs
        app.state.affiliateURLs = affiliateURLs
                
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

