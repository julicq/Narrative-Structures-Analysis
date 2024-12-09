FROM python:3.11-slim

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
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

# Создаем структуру директорий
RUN mkdir -p /app /app/db
WORKDIR /app

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version && \
    poetry config virtualenvs.create false

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Генерируем новый poetry.lock на основе pyproject.toml
RUN poetry lock --no-update

# Установка зависимостей
RUN poetry install --only main --no-interaction --no-ansi

# Создаем пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app

# Копируем код приложения
COPY . .

# Загружаем модель spaCy
RUN python -m spacy download en_core_web_sm

# Настраиваем права для директории db
RUN chmod -R 777 /app/db

USER appuser

CMD ["python", "run_bot.py"]
