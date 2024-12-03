# shared/config.py

from enum import Enum
from typing import Optional
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class ModelType(str, Enum):
    GIGACHAT = "gigachat"
    OPENAI = "openai"
    OLLAMA = "ollama"

def debug_env_value(key: str, default: str = None) -> str:
    """Get environment variable value with debug information."""
    value = os.getenv(key, default)
    if value:
        value = value.split('#')[0].strip()
    print(f"Loading {key}={value}")
    return value

class Config(BaseSettings):
    # Базовые настройки
    debug: bool = Field(default=False)

    # Flask конфигурация
    flask_host: str = Field(default='0.0.0.0')
    flask_port: int = Field(default=5001)
    flask_env: str = Field(default='development')
    secret_key: str = Field(default='your-secret-key')

    # Telegram конфигурация
    telegram_token: str = Field(...)  # Required field

    # Активная модель - исправленное определение
    active_model: str = Field(
        default="ollama",
        env="ACTIVE_MODEL"
    )

    @property
    def active_model_type(self) -> ModelType:
        return ModelType(self.active_model.lower())

    # Настройки Ollama
    ollama_model_name: str = Field(default='llama3.2')
    ollama_base_url: str = Field(default='http://localhost:11434')

    # Настройки GigaChat
    gigachat_client_id: Optional[str] = None
    gigachat_client_secret: Optional[str] = None
    gigachat_verify_ssl: bool = Field(default=False)
    gigachat_model_name: str = Field(default='GigaChat:latest')
    gigachat_scope: str = Field(default='GIGACHAT_API_PERS')
    gigachat_base_url: str = Field(
        default='https://gigachat.devices.sberbank.ru/api/v1'
    )
    gigachat_auth_url: str = Field(
        default='https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    )
    gigachat_token: Optional[str] = None
    gigachat_cert: Optional[str] = None

    # Настройки OpenAI
    openai_api_key: Optional[str] = None
    openai_model_name: str = Field(default='gpt-4')
    openai_organization: Optional[str] = None

    # Общие ограничения API
    max_text_length: int = Field(default=10000)
    request_timeout: int = Field(default=300)
    max_retries: int = Field(default=3)
    retry_delay: int = Field(default=1)

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        use_enum_values=True,
        env_prefix="",
        extra="ignore"
    )

    def get_model_credentials(self, model_type: ModelType) -> Optional[dict]:
        """Получение учетных данных для конкретной модели"""
        credentials = {
            ModelType.GIGACHAT: {
                'client_id': self.gigachat_client_id,
                'client_secret': self.gigachat_client_secret,
                'verify_ssl': self.gigachat_verify_ssl,
                'model_name': self.gigachat_model_name,
                'base_url': self.gigachat_base_url,
                'auth_url': self.gigachat_auth_url,
                'scope': self.gigachat_scope
            },
            ModelType.OPENAI: {
                'api_key': self.openai_api_key,
                'model_name': self.openai_model_name,
                'organization': self.openai_organization
            },
            ModelType.OLLAMA: {
                'model_name': self.ollama_model_name,
                'base_url': self.ollama_base_url
            }
        }
        return credentials.get(model_type)

    def validate_model_credentials(self, model_type: ModelType) -> bool:
        """Проверка наличия необходимых учетных данных для модели"""
        credentials = self.get_model_credentials(model_type)
        if not credentials:
            return False

        required_fields = {
            ModelType.GIGACHAT: ['client_id', 'client_secret'],
            ModelType.OPENAI: ['api_key'],
            ModelType.OLLAMA: ['base_url']
        }

        return all(
            credentials.get(field) is not None 
            for field in required_fields[model_type]
        )

# Create a global instance
settings = Config()