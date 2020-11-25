FROM python:3.8.5-slim as builder

COPY ./requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install gcc git -y \
    && apt-get clean \
    && pip install --user --no-cache-dir -r requirements.txt

FROM python:3.8.5-slim as app

ARG COMMIT_HASH
ENV COMMIT_HASH=$COMMIT_HASH
ENV DD_VERSION=$COMMIT_HASH

COPY --from=builder /root/.local /root/.local
COPY src /app

WORKDIR /app

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8090

CMD ["gunicorn", "--bind", ":8090", "--workers", "3", "cookbook.wsgi"]
