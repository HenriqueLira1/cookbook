FROM python:3.8.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
COPY requirements-dev.txt /app/

RUN pip install -r requirements-dev.txt
COPY . /app/

ENV PYTHONPATH=/app/src:$PYTHONPATH

EXPOSE 8090
