FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry install --no-root --no-interaction --no-ansi

RUN pwd && ls -l /app

EXPOSE 8000

CMD ["sh", "-c", "cd /app && poetry run alembic upgrade head && poetry run uvicorn --host 0.0.0.0 --port 8000 tech.api.app:app"]
