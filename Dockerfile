# Базовый образ с точной версией Python
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

# Установка Poetry с проверкой
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version && \
    poetry config virtualenvs.create false

# Проверяем установку Poetry и окружение
RUN which poetry && \
    echo $PATH && \
    ls -la /opt/poetry/bin

# Устанавливаем рабочую директорию
WORKDIR /app

# Создаем тестовый файл для проверки
RUN echo "print('Test successful')" > test.py && \
    python test.py

# Создаем тестовый pyproject.toml для проверки
RUN echo '[tool.poetry]\nname = "test-project"\nversion = "0.1.0"\ndescription = ""\nauthors = ["Test <test@example.com>"]\n\n[tool.poetry.dependencies]\npython = "^3.11"\n' > pyproject.toml && \
    echo "" > poetry.lock

# Пробуем выполнить простую команду poetry
RUN poetry check

# Если все успешно, продолжаем с основными файлами
COPY pyproject.toml poetry.lock ./

# Остальные команды закомментированы для отладки
#RUN poetry install --only main --no-interaction --no-ansi -vvv

#RUN groupadd -r appuser && useradd -r -g appuser appuser \
#    && chown -R appuser:appuser /app

#COPY . .
#RUN python -m spacy download en_core_web_sm
#RUN chmod -R 777 /app/db

USER appuser
# Запускаем приложение
CMD ["python", "run_bot.py"]
