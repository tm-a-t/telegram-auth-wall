FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STATIC_DIR=dist

WORKDIR /app/
RUN pip install --no-cache-dir poetry==1.6
COPY server/poetry.lock server/pyproject.toml ./

RUN apt-get update -y
RUN poetry export -f requirements.txt | pip install --no-cache-dir -r /dev/stdin

COPY server/ .
COPY .vitepress/dist dist
