FROM python:3.11-slim

WORKDIR /code

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

ENV GOOGLE_APPLICATION_CREDENTIALS /code/app/weblab-morning-firebase-adminsdk-c5y5g-f68c90538e.json
