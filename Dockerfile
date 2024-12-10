FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry>=1.7.1"

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-interaction --no-ansi

COPY . .

RUN python -m spacy download en_core_web_sm

RUN mkdir -p /app/db

RUN chmod -R 777 /app/db

EXPOSE 8000

CMD ["python", "run_bot.py"]
