FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt  /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app