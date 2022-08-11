FROM python:3.10.4

LABEL Author="Ivan Trushin"

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN mkdir "/app"

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt