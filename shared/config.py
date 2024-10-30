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

    # Telegram конфигурация
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Активная модель
    ACTIVE_MODEL: ModelType = ModelType(os.getenv('ACTIVE_MODEL', 'gigachat').lower())

    # Настройки Ollama
    OLLAMA_MODEL_NAME: str = os.getenv('OLLAMA_MODEL_NAME', 'llama3.2')
    OLLAMA_BASE_URL: str = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

    # Настройки GigaChat
    GIGACHAT_CLIENT_ID: Optional[str] = os.getenv('GIGACHAT_CLIENT_ID')
    GIGACHAT_CLIENT_SECRET: Optional[str] = os.getenv('GIGACHAT_CLIENT_SECRET')
    GIGACHAT_VERIFY_SSL: bool = os.getenv('GIGACHAT_VERIFY_SSL', 'True') == 'True'
    GIGACHAT_MODEL_NAME: str = os.getenv('GIGACHAT_MODEL_NAME', 'GigaChat:latest')
    GIGACHAT_SCOPE: str = os.getenv('GIGACHAT_SCOPE', 'GIGACHAT_API_PERS')
    GIGACHAT_BASE_URL: str = os.getenv(
        'GIGACHAT_BASE_URL', 
        'https://gigachat.devices.sberbank.ru/api/v1'
    )
    GIGACHAT_AUTH_URL: str = os.getenv(
        'GIGACHAT_AUTH_URL',
        'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    )
    GIGACHAT_CREDENTIALS: str = os.getenv('GIGACHAT_CREDENTIALS')

    # Настройки OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL_NAME: str = os.getenv('OPENAI_MODEL_NAME', 'gpt-4')
    OPENAI_ORGANIZATION: Optional[str] = os.getenv('OPENAI_ORGANIZATION')

    # Настройки Anthropic
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
    ANTHROPIC_MODEL_NAME: str = os.getenv('ANTHROPIC_MODEL_NAME', 'claude-3')

    # Общие ограничения API
    MAX_TEXT_LENGTH: int = int(os.getenv('MAX_TEXT_LENGTH', '10000'))
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '300'))
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY: int = int(os.getenv('RETRY_DELAY', '1'))

    @classmethod
    def get_model_credentials(cls, model_type: ModelType) -> Optional[dict]:
        """Получение учетных данных для конкретной модели"""
        credentials = {
            ModelType.GIGACHAT: {
                'client_id': cls.GIGACHAT_CLIENT_ID,
                'client_secret': cls.GIGACHAT_CLIENT_SECRET,
                'verify_ssl': cls.GIGACHAT_VERIFY_SSL,
                'model_name': cls.GIGACHAT_MODEL_NAME,
                'base_url': cls.GIGACHAT_BASE_URL,
                'auth_url': cls.GIGACHAT_AUTH_URL,
                'scope': cls.GIGACHAT_SCOPE
            },
            ModelType.OPENAI: {
                'api_key': cls.OPENAI_API_KEY,
                'model_name': cls.OPENAI_MODEL_NAME,
                'organization': cls.OPENAI_ORGANIZATION
            },
            ModelType.ANTHROPIC: {
                'api_key': cls.ANTHROPIC_API_KEY,
                'model_name': cls.ANTHROPIC_MODEL_NAME
            },
            ModelType.OLLAMA: {
                'model_name': cls.OLLAMA_MODEL_NAME,
                'base_url': cls.OLLAMA_BASE_URL
            }
        }
        return credentials.get(model_type)

    @classmethod
    def validate_model_credentials(cls, model_type: ModelType) -> bool:
        """Проверка наличия необходимых учетных данных для модели"""
        credentials = cls.get_model_credentials(model_type)
        if not credentials:
            return False

        required_fields = {
            ModelType.GIGACHAT: ['client_id', 'client_secret'],
            ModelType.OPENAI: ['api_key'],
            ModelType.ANTHROPIC: ['api_key'],
            ModelType.OLLAMA: ['base_url']
        }

        return all(
            credentials.get(field) is not None 
            for field in required_fields[model_type]
        )
