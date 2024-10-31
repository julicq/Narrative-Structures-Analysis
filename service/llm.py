# service/llm.py

import base64
from typing import Optional, Union, Dict, Any, List, Tuple
import uuid
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from pydantic import Field, BaseModel, ConfigDict
from langchain_core.callbacks.base import BaseCallbackHandler
import logging
from enum import Enum, auto
import os
from dotenv import load_dotenv
import urllib3
import requests
from shared.config import Config
import time

# Отключаем предупреждения о небезопасном SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Загружаем переменные окружения
load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelType(str, Enum):
    """Поддерживаемые типы моделей"""
    OPENAI = auto()
    GIGACHAT = auto()
    OLLAMA = auto()
    ANTHROPIC = auto()

class GigaChatConfig(BaseModel):
    """Конфигурация для GigaChat API"""

    model_config = ConfigDict(protected_namespaces=())
    
    client_id: str
    client_secret: str
    verify_ssl: bool = False
    auth_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    base_url: str = "https://gigachat.devices.sberbank.ru/api/v1"
    scope: str = "GIGACHAT_API_PERS"
    model_name: str = "GigaChat:latest"
    api_version: str = "v1"
    cert_path: Optional[str] = None

class CustomGigaChat(BaseChatModel):
    """Кастомная реализация GigaChat"""
    
    config: GigaChatConfig = Field(...)
    temperature: float = Field(default=0.7)
    access_token: Optional[str] = Field(default=None)
    
    @property
    def _llm_type(self) -> str:
        """Возвращает тип LLM модели"""
        return "gigachat"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Возвращает параметры для идентификации модели"""
        return {
            "model_name": self.config.model_name,
            "temperature": self.temperature,
        }

    def __init__(self, **kwargs):
        # Получаем учетные данные из переменных окружения
        client_id = os.getenv('GIGACHAT_CLIENT_ID')
        client_secret = os.getenv('GIGACHAT_CLIENT_SECRET')

        if not client_id or not client_secret:
            raise ValueError("GIGACHAT_CLIENT_ID and GIGACHAT_CLIENT_SECRET must be set in environment variables")
            
        # Создаем конфигурацию
        config = GigaChatConfig(
            client_id=client_id,
            client_secret=client_secret,
        )
        
        # Инициализируем базовый класс
        super().__init__(
            config=config,
            temperature=kwargs.get('temperature', 0.7)
        )
        
        # Получаем токен доступа
        self._get_access_token()

    def _get_access_token(self) -> None:
        """Получение токена доступа"""
        response = None  # Инициализируем response здесь
        try:
            credentials = base64.b64encode(
                f"{self.config.client_id}:{self.config.client_secret}".encode('utf-8')
            ).decode('utf-8')

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': str(uuid.uuid4()),
                'Authorization': f'Basic {credentials}'
            }

            response = requests.post(
                self.config.auth_url,
                headers=headers,
                data=f'scope={self.config.scope}',
                verify=False
            )

            logger.debug(f"Auth response status: {response.status_code}")
            logger.debug(f"Auth response content: {response.text}")

            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get access token: {str(e)}")
            if response and hasattr(response, 'text'):
                logger.error(f"Response content: {response.text}")
            raise  # Перебрасываем исключение дальше


    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Генерация ответа на основе сообщений"""
        if not self.access_token:
            self._get_access_token()

        formatted_messages = [
            {
                "role": "user" if isinstance(msg, HumanMessage) else "assistant",
                "content": msg.content
            }
            for msg in messages
        ]

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        payload = {
            "model": self.config.model_name,
            "messages": formatted_messages,
            "temperature": self.temperature,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.config.base_url}/chat/completions",
                headers=headers,
                json=payload,
                verify=False
            )
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0]['message']
                generation = ChatGeneration(
                    message=AIMessage(content=message['content']),
                    generation_info={"finish_reason": result['choices'][0].get('finish_reason')}
                )
                return ChatResult(generations=[generation])
            else:
                raise ValueError("No valid response from GigaChat")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in GigaChat API call: {str(e)}")
            logger.error(f"Response content: {getattr(e.response, 'text', 'No response content')}")
            raise

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Асинхронная версия _generate"""
        raise NotImplementedError("Async generation not implemented for GigaChat")


class ModelAvailability:
    """Класс для отслеживания доступности моделей"""
    
    def __init__(self):
        self.status: Dict[ModelType, bool] = {
            model_type: True for model_type in ModelType
        }
        self.last_check: Dict[ModelType, float] = {
            model_type: 0 for model_type in ModelType
        }
        self.check_interval: float = 60  # seconds

    def should_check(self, model_type: ModelType) -> bool:
        """Проверяет, нужно ли обновить статус модели"""
        return time.time() - self.last_check[model_type] > self.check_interval

    def update_status(self, model_type: ModelType, available: bool):
        """Обновляет статус доступности модели"""
        self.status[model_type] = available
        self.last_check[model_type] = time.time()

class LLMFactory:
    """Фабрика для создания экземпляров различных LLM моделей"""
    
    DEFAULT_MODELS = {
        ModelType.OLLAMA: "llama2",
        ModelType.OPENAI: "gpt-4",
        ModelType.GIGACHAT: "GigaChat:latest",
        ModelType.ANTHROPIC: "claude-3-opus-20240229"
    }

    FALLBACK_CHAIN = {
        ModelType.OLLAMA: ModelType.GIGACHAT,
        ModelType.OPENAI: ModelType.GIGACHAT,
        ModelType.ANTHROPIC: ModelType.GIGACHAT,
        ModelType.GIGACHAT: None  # Конечная точка fallback
    }

    @staticmethod
    def check_availability(model_type: ModelType) -> bool:
        """Проверяет доступность модели"""
        try:
            if model_type == ModelType.OLLAMA:
                response = requests.get("http://localhost:11434/api/health", timeout=2)
                return response.status_code == 200
            elif model_type == ModelType.GIGACHAT:
                # Проверяем наличие переменных окружения
                return bool(os.getenv('GIGACHAT_CLIENT_ID') and 
                          os.getenv('GIGACHAT_CLIENT_SECRET'))
            elif model_type == ModelType.OPENAI:
                return bool(os.getenv('OPENAI_API_KEY'))
            elif model_type == ModelType.ANTHROPIC:
                return bool(os.getenv('ANTHROPIC_API_KEY'))
            elif model_type == ModelType.OPENAI:
                return bool(os.getenv('OPENAI_API_KEY'))
            elif model_type == ModelType.ANTHROPIC:
                return bool(os.getenv('ANTHROPIC_API_KEY'))
        except Exception as e:
            logger.error(f"Error checking availability for {model_type}: {str(e)}")
            return False
        return False

    @staticmethod
    def create_llm(
        model_type: Union[ModelType, str],
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        streaming: bool = True,
        try_fallback: bool = True,
        **kwargs
    ) -> Tuple[BaseLanguageModel, ModelType]:
        """Создает экземпляр LLM модели указанного типа с поддержкой fallback"""
        if isinstance(model_type, str):
            try:
                model_type = ModelType(model_type)
            except ValueError:
                raise ValueError(f"Unsupported model type: {model_type}")

        callbacks = [StreamingStdOutCallbackHandler()] if streaming else []
        callback_manager = CallbackManager(callbacks)
        model_name = model_name or LLMFactory.DEFAULT_MODELS[model_type]

        try:
            # Проверяем доступность модели
            if not LLMFactory.check_availability(model_type):
                raise ConnectionError(f"{model_type} is not available")

            if model_type == ModelType.GIGACHAT:
                cert_path = os.getenv('GIGACHAT_CERT')
                if not cert_path:
                    raise ValueError("GIGACHAT_CERT environment variable is not set")
                if not os.path.exists(cert_path):
                    raise FileNotFoundError(f"Certificate file not found at {cert_path}")
                
                config = GigaChatConfig(
                    client_id=os.getenv('GIGACHAT_CLIENT_ID'),
                    client_secret=os.getenv('GIGACHAT_CLIENT_SECRET'),
                    verify_ssl=False,  # Используем путь к сертификату
                    cert_path=cert_path
                )
                model = CustomGigaChat(
                    config=config,
                    temperature=temperature,
                    **kwargs
                )
            elif model_type == ModelType.OLLAMA:
                model = OllamaLLM(
                    model=model_name,
                    callback_manager=callback_manager,
                    temperature=temperature,
                    base_url="http://localhost:11434",
                    **kwargs
                )
            elif model_type == ModelType.OPENAI:
                model = ChatOpenAI(
                    model_name=model_name,
                    temperature=temperature,
                    streaming=streaming,
                    api_key=os.getenv("OPENAI_API_KEY"),
                    **kwargs
                )
            elif model_type == ModelType.ANTHROPIC:
                model = ChatAnthropic(
                    model=model_name,
                    temperature=temperature,
                    streaming=streaming,
                    api_key=os.getenv("ANTHROPIC_API_KEY"),
                    **kwargs
                )
            return model, model_type

        except Exception as e:
            logger.error(f"Error creating {model_type} instance: {str(e)}")
            if try_fallback:
                fallback_type = LLMFactory.FALLBACK_CHAIN.get(model_type)
                if fallback_type:
                    logger.info(f"Falling back to {fallback_type}")
                    return LLMFactory.create_llm(
                        fallback_type,
                        temperature=temperature,
                        streaming=streaming,
                        try_fallback=True,
                        **kwargs
                    )
            raise

class LLMManager:
    """Менеджер для работы с несколькими LLM моделями"""
    
    def __init__(self):
        self.models: Dict[str, BaseLanguageModel] = {}
        self.model_types: Dict[str, ModelType] = {}
        self.default_model: Optional[str] = None
        self.availability = ModelAvailability()

    def add_model(
        self,
        model_type: Union[ModelType, str],
        model_name: Optional[str] = None,
        alias: Optional[str] = None,
        make_default: bool = False,
        **kwargs
    ) -> BaseLanguageModel:
        """Добавляет модель в менеджер"""
        model, actual_type = LLMFactory.create_llm(model_type, model_name, **kwargs)
        
        if not alias:
            if isinstance(model_type, str):
                model_type = ModelType(model_type.lower())
            model_name = model_name or LLMFactory.DEFAULT_MODELS[model_type]
            alias = f"{actual_type.value}_{model_name}"
            
        self.models[alias] = model
        self.model_types[alias] = actual_type
        
        if make_default or not self.default_model:
            self.default_model = alias
            
        return model

    def get_model(self, alias: Optional[str] = None) -> BaseLanguageModel:
        """Получает модель по псевдониму с поддержкой fallback"""
        if not alias:
            if not self.default_model:
                raise ValueError("No default model set")
            alias = self.default_model
            
        if alias not in self.models:
            raise KeyError(f"Model with alias '{alias}' not found")

        model_type = self.model_types[alias]
        
        # Проверяем доступность модели
        if self.availability.should_check(model_type):
            available = LLMFactory.check_availability(model_type)
            self.availability.update_status(model_type, available)
            
            if not available:
                # Пробуем создать fallback модель
                fallback_type = LLMFactory.FALLBACK_CHAIN.get(model_type)
                if fallback_type:
                    try:
                        model, actual_type = LLMFactory.create_llm(
                            fallback_type,
                            try_fallback=True
                        )
                        self.models[alias] = model
                        self.model_types[alias] = actual_type
                        return model
                    except Exception as e:
                        logger.error(f"Fallback failed: {str(e)}")
                        
        return self.models[alias]

def initialize_llm(
    model_type: Union[ModelType, str] = ModelType.OLLAMA,
    model_name: Optional[str] = None,
    **kwargs
) -> BaseLanguageModel:
    """Инициализирует одиночную модель LLM с поддержкой fallback"""
    model, _ = LLMFactory.create_llm(model_type, model_name, **kwargs)
    return model