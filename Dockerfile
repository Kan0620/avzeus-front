FROM python:3.8

COPY requirements.txt .

RUN pip install -U pip && pip install  -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]