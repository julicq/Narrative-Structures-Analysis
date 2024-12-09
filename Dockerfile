# Базовый образ с точной версией Python
FROM python:3.11-slim

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем непривилегированного пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Создаем и настраиваем директории
RUN mkdir -p /app /app/db && \
    chown -R appuser:appuser /app

# Установка Poetry через официальный установщик
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    chmod +x /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

# Копируем файлы зависимостей
COPY --chown=appuser:appuser pyproject.toml poetry.lock ./

# Переключаемся на непривилегированного пользователя
USER appuser

# Установка зависимостей
RUN poetry install --only main --no-interaction --no-ansi

# Копируем код приложения
COPY --chown=appuser:appuser . .

# Загружаем модель spaCy
RUN python -m spacy download en_core_web_sm

# Настраиваем права для директории db
USER root
RUN chmod -R 777 /app/db
USER appuser

# Запускаем приложение
CMD ["python", "run_bot.py"]
