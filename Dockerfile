# Базовый образ с точной версией Python
FROM python:3.11-slim

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Создаем непривилегированного пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Установка Poetry
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Отключаем создание виртуального окружения
RUN poetry config virtualenvs.create false

# Создаем и настраиваем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY --chown=appuser:appuser pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry install --only main --no-interaction --no-ansi

# Копируем код приложения
COPY --chown=appuser:appuser . .

# Загружаем модель spaCy
RUN python -m spacy download en_core_web_sm

# Создаем необходимые директории и настраиваем права
RUN mkdir -p /app/db && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod -R 777 /app/db

# Переключаемся на непривилегированного пользователя
USER appuser

# Запускаем приложение
CMD ["python", "run_bot.py"]
