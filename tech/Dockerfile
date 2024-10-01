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

RUN chmod +x /usr/local/bin/poetry
RUN chmod -R 755 /root/.local/share/pypoetry
RUN chmod +x /app/entrypoint.sh

RUN poetry config installer.max-workers 10

RUN poetry install --no-root --no-interaction --no-ansi

RUN chmod -R 755 /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "tech.core.app.app:app"]
