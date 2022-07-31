from typing import Callable
import os

from fastapi import FastAPI


def _startup_model(app: FastAPI) -> None:
    with open("app/static/raw_cut.js", "r") as raw_cut:
        CUT_URL = os.environ["CUT_URL"]
        print(CUT_URL)
        code = raw_cut.read()
        with open("app/static/cut.js", "w") as cut:
            code = code.replace("CUT_URL", CUT_URL)
            cut.write(code)
    with open("app/static/raw_predict.js", "r") as raw_cut:
        PREDICT_URL = os.environ["PREDICT_URL"]
        print(CUT_URL)
        code = raw_cut.read()
        with open("app/static/predict.js", "w") as cut:
            code = code.replace("PREDICT_URL", PREDICT_URL)
            cut.write(code)
            
def _shutdown_model(app: FastAPI) -> None:
    os.remove("app/static/cut.js")
    os.remove("app/static/predict.js")
    


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        _startup_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        _shutdown_model(app)

    return shutdown
