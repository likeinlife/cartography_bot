FROM python:3.11.8-alpine3.19

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src .

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ./docker-entrypoint.sh