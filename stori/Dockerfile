FROM python:3.10-slim-bookworm AS core

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.6.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update \
  && pip install "poetry==$POETRY_VERSION" \
  && poetry --version

WORKDIR /stori
COPY . /stori
RUN poetry install
CMD python manage.py runserver 0.0.0.0:8000
