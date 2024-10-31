# service/llm.py

import base64
from typing import Optional, Union, Dict, Any, List
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

    # Отключаем предупреждение о конфликте имен
    model_config = ConfigDict(protected_namespaces=())
    
    client_id: str
    client_secret: str
    verify_ssl: bool = Field(default_factory=lambda: Config.GIGACHAT_VERIFY_SSL)
    auth_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    base_url: str = "https://gigachat.devices.sberbank.ru/api/v1"
    scope: str = "GIGACHAT_API_PERS"
    model_name: str = "GigaChat:latest"
    api_version: str = "v1"

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
                verify=self.config.verify_ssl
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
            raise

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
                verify=self.config.verify_ssl
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


class LLMFactory:
    """Фабрика для создания экземпляров различных LLM моделей"""
    
    DEFAULT_MODELS = {
        ModelType.OLLAMA: "llama3.2",
        ModelType.OPENAI: "gpt-4",
        ModelType.GIGACHAT: "GigaChat:latest",
        ModelType.ANTHROPIC: "claude-3-opus-20240229"
    }

    @staticmethod
    def create_llm(
        model_type: Union[ModelType, str],
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        streaming: bool = True,
        **kwargs
    ) -> BaseLanguageModel:
        """Создает экземпляр LLM модели указанного типа"""
        
        if isinstance(model_type, str):
            try:
                model_type = ModelType(model_type)
            except ValueError:
                raise ValueError(f"Unsupported model type: {model_type}")

        callbacks = [StreamingStdOutCallbackHandler()] if streaming else []
        callback_manager = CallbackManager(callbacks)

        model_name = model_name or LLMFactory.DEFAULT_MODELS[model_type]

        try:
            if model_type == ModelType.OLLAMA:
                return OllamaLLM(
                    model=model_name,
                    callback_manager=callback_manager,
                    temperature=temperature,
                    base_url="http://localhost:11434",
                    **kwargs
                )
                
            elif model_type == ModelType.OPENAI:
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY not found in environment variables")
                    
                return ChatOpenAI(
                    model_name=model_name,
                    temperature=temperature,
                    streaming=streaming,
                    api_key=api_key,
                    **kwargs
                )
                
            elif model_type == ModelType.ANTHROPIC:
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
                    
                return ChatAnthropic(
                    model=model_name,
                    temperature=temperature,
                    streaming=streaming,
                    api_key=api_key,
                    **kwargs
                )
            
            elif model_type == ModelType.GIGACHAT:
                return CustomGigaChat(
                    temperature=temperature,
                    **kwargs
                )

        except Exception as e:
            logger.error(f"Error creating LLM instance: {str(e)}")
            raise

class LLMManager:
    """Менеджер для работы с несколькими LLM моделями"""
    
    def __init__(self):
        self.models: Dict[str, BaseLanguageModel] = {}
        self.default_model: Optional[str] = None

    def add_model(
        self,
        model_type: Union[ModelType, str],
        model_name: Optional[str] = None,
        alias: Optional[str] = None,
        make_default: bool = False,
        **kwargs
    ) -> BaseLanguageModel:
        """Добавляет модель в менеджер"""
        model = LLMFactory.create_llm(model_type, model_name, **kwargs)
        
        if not alias:
            if isinstance(model_type, str):
                model_type = ModelType(model_type.lower())
            model_name = model_name or LLMFactory.DEFAULT_MODELS[model_type]
            alias = f"{model_type.value}_{model_name}"
            
        self.models[alias] = model
        
        if make_default or not self.default_model:
            self.default_model = alias
            
        return model

    def get_model(self, alias: Optional[str] = None) -> BaseLanguageModel:
        """Получает модель по псевдониму"""
        if not alias:
            if not self.default_model:
                raise ValueError("No default model set")
            alias = self.default_model
            
        if alias not in self.models:
            raise KeyError(f"Model with alias '{alias}' not found")
            
        return self.models[alias]

def initialize_llm(
    model_type: Union[ModelType, str] = ModelType.OLLAMA,
    model_name: Optional[str] = None,
    **kwargs
) -> BaseLanguageModel:
    """Инициализирует одиночную модель LLM"""
    return LLMFactory.create_llm(model_type, model_name, **kwargs)