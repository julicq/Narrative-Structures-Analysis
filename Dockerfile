FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python -m spacy download en_core_web_sm

EXPOSE 8000

CMD ["python", "run_bot.py"]
