FROM python:3.11.5-slim-bookworm

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

RUN mkdir /code

WORKDIR /code

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry

RUN poetry install --no-root

COPY . .

# RUN chmod +x docker/app/app.sh/
#
# RUN chmod +x docker/celery_app.sh/
