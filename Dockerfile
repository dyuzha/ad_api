FROM python:3.13-slim AS builder

LABEL maintainer="Dyuzhev Matvey"

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
ENV POETRY_VERSION=2.1.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    # Создаем символическую ссылку для глобального доступа
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Устанавливаем плагин poetry
RUN poetry self add poetry-plugin-export

WORKDIR /src/ad_api

# Сначала копируем только файлы зависимостей (Для кеширования)
COPY ./pyproject.toml ./poetry.lock ./

# Генерируем requirements.txt с разделением dev и prod
RUN poetry export --without-hashes --only=main --no-interaction -f requirements.txt -o requirements.txt
RUN poetry export --without-hashes --only=dev --no-interaction -f requirements.txt -o requirements-dev.txt


FROM python:3.13-slim AS production

LABEL maintainer="Dyuzhev Matvey"

WORKDIR /src

# Устанавливаем зависимости
COPY --from=builder /src/ad_api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env ./..

# Копируем остальные файлы приложения
COPY ./src/ad_api ./ad_api
COPY ./src/main.py .

COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
