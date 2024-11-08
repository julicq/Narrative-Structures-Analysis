# shared/config.py

from enum import Enum
import json
from typing import Optional
import os
from dotenv import load_dotenv
from shared.constants import DASHBOARD_CONFIG_DIR, ModelType

load_dotenv()

class ModelType(Enum):
    GIGACHAT = "gigachat"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"

def debug_env_value(key: str, default: str = None) -> str:
    """Get environment variable value with debug information."""
    value = os.getenv(key, default)
    if value:
        # Убираем комментарии и лишние пробелы
        value = value.split('#')[0].strip()
    print(f"Loading {key}={value}")
    return value

class Config:
    # Базовые настройки
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'

    # Настройки для дашборда
    DASHBOARD_CONFIG_DIR: str = os.getenv('DASHBOARD_CONFIG_DIR', 'config')
    SELECTED_MODELS_FILE: str = os.path.join(DASHBOARD_CONFIG_DIR, 'selected_models.json')
    BOT_MESSAGES_FILE: str = os.path.join(DASHBOARD_CONFIG_DIR, 'bot_messages.json')

    # Flask конфигурация
    FLASK_HOST: str = '0.0.0.0'
    FLASK_PORT: int = 5001
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

    # Telegram конфигурация
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Активная модель - используем debug_env_value для отладки
    ACTIVE_MODEL: ModelType = ModelType(debug_env_value('ACTIVE_MODEL', 'gigachat').lower())

    # Настройки Ollama
    OLLAMA_MODEL_NAME: str = os.getenv('OLLAMA_MODEL_NAME', 'llama3.2')
    OLLAMA_BASE_URL: str = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

    # Настройки GigaChat
    GIGACHAT_CLIENT_ID: Optional[str] = os.getenv('GIGACHAT_CLIENT_ID')
    GIGACHAT_CLIENT_SECRET: Optional[str] = os.getenv('GIGACHAT_CLIENT_SECRET')
    GIGACHAT_VERIFY_SSL: bool = os.getenv('GIGACHAT_VERIFY_SSL', 'False').lower() == 'true'
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
    GIGACHAT_TOKEN: str = os.getenv('GIGACHAT_TOKEN')
    GIGACHAT_CERT: str = os.getenv('GIGACHAT_CERT')

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

    @staticmethod
    def get_selected_models():
        file_path = os.path.join(DASHBOARD_CONFIG_DIR, 'selected_models.json')
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            # Инициализируем файл данными по умолчанию
            default_models = [model_type.value for model_type in ModelType]
            with open(file_path, 'w') as f:
                json.dump(default_models, f)
            return default_models
        
        with open(file_path, 'r') as f:
            return json.load(f)
        
    @staticmethod
    def set_selected_models(models):
        file_path = os.path.join(Config.DASHBOARD_CONFIG_DIR, 'selected_models.json')
        with open(file_path, 'w') as f:
            json.dump([model.value for model in models], f)

    @classmethod
    def get_bot_message(cls, message_type: str) -> str:
        """Получение сообщения бота по типу"""
        messages = cls.get_bot_messages()
        return messages.get(message_type, "")

    @classmethod
    def set_bot_message(cls, message_type: str, message: str):
        """Установка сообщения бота по типу"""
        messages = cls.get_bot_messages()
        messages[message_type] = message
        cls.set_bot_messages(messages)

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
    def validate(cls):
        """Проверка конфигурации"""
        if not cls.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN не установлен")
            
        if cls.ACTIVE_MODEL == ModelType.GIGACHAT and not cls.GIGACHAT_TOKEN:
            raise ValueError("GIGACHAT_TOKEN не установлен, но выбрана модель GIGACHAT")
        
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

    @classmethod
    def get_bot_messages(cls):
        file_path = os.path.join(DASHBOARD_CONFIG_DIR, 'bot_messages.json')
        if not os.path.exists(file_path):
            # Создаем файл с сообщениями по умолчанию, если он не существует
            default_messages = {
                'welcome': 'Добро пожаловать!',
                'goodbye': 'До свидания!',
                # Добавьте другие сообщения по умолчанию
            }
            with open(file_path, 'w') as f:
                json.dump(default_messages, f)
            return default_messages
        
        with open(file_path, 'r') as f:
            return json.load(f)

    @classmethod
    def set_bot_message(cls, message_type, message):
        messages = cls.get_bot_messages()
        messages[message_type] = message
        file_path = os.path.join(DASHBOARD_CONFIG_DIR, 'bot_messages.json')
        with open(file_path, 'w') as f:
            json.dump(messages, f)