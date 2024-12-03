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

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt
COPY requirements_exact.txt requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY . .

# Создаем необходимые директории
RUN mkdir -p /app/db

# Устанавливаем права
RUN chmod -R 777 /app/db

# Запускаем приложение
CMD ["python", "run_bot.py"]