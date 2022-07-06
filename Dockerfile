FROM python:3.8.13

COPY requirements.txt .

RUN pip install -U pip && pip install  -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "local_main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]