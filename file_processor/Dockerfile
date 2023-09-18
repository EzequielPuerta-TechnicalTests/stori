FROM python:3.10-slim-bookworm AS file_processor

ENV PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.6.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update \
  && pip install "poetry==$POETRY_VERSION" \
  && poetry --version

WORKDIR /file_processor
COPY . /file_processor
RUN poetry install

ENTRYPOINT celery -A processor worker --autoscale 10 --loglevel=info
