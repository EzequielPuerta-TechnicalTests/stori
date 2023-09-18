FROM python:3.10-slim-bookworm AS task_manager

ENV PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.6.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update \
  && pip install "poetry==$POETRY_VERSION" \
  && poetry --version

WORKDIR /task_manager
COPY . /task_manager
RUN poetry install

ENTRYPOINT python main.py
