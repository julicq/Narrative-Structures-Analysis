# Базовый образ с точной версией Python
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*



# Копируем код проекта
RUN pip install "poetry>=1.7.1"

# Configure poetry
RUN poetry config virtualenvs.create false

# Создаем рабочую директорию
WORKDIR /app


COPY pyproject.toml poetry.lock ./
# Install dependencies with specific flags
RUN poetry install --only main --no-interaction --no-ansi

COPY . .
# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Создаем необходимые директории
RUN mkdir -p /app/db

# Устанавливаем права
RUN chmod -R 777 /app/db

# Запускаем приложение
CMD ["python", "run_bot.py"]