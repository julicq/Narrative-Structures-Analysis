# Базовый образ с точной версией Python
FROM python:3.11-slim


# Создаем рабочую директорию
WORKDIR /app

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

# Устанавливаем Poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.7.1
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

COPY pyproject.toml poetry.lock ./
# Install dependencies with specific flags
RUN poetry install --only main --no-interaction --no-ansi

COPY . .
# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Создаем необходимые директории
RUN mkdir -p /app/db && \
    chown -R appuser:appuser /app

USER appuser

# Запускаем приложение
CMD ["python", "run_bot.py"]