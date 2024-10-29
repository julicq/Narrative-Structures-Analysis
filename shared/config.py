# shared/config.py

from enum import Enum
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class ModelType(Enum):
    GIGACHAT = "gigachat"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"

class Config:
    # Flask конфигурация
    FLASK_HOST: str = '0.0.0.0'
    FLASK_PORT: int = 5001
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

    OLLAMA_MODEL_NAME = "llama3.2"  # или другая модель
    OLLAMA_BASE_URL = "http://localhost:11434"

    # Telegram конфигурация
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Модели
    ACTIVE_MODEL: ModelType = ModelType.OLLAMA

    # API ключи
    GIGACHAT_CREDENTIALS: Optional[str] = os.getenv('GIGACHAT_CREDENTIALS')
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY')

    # Настройки моделей
    OPENAI_MODEL_NAME: str = "gpt-4"
    ANTHROPIC_MODEL_NAME: str = "claude-3.5"

    # Ограничения API
    MAX_TEXT_LENGTH: int = 10000
    REQUEST_TIMEOUT: int = 300
