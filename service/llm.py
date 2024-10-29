# service/llm.py

from typing import Optional, Union, Dict, Any
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from gigachat import GigaChat
from langchain_anthropic import ChatAnthropic
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from pydantic import BaseModel
from langchain_core.language_models.base import BaseLanguageModel
import logging
from enum import Enum
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

logger = logging.getLogger(__name__)

class ModelType(Enum):
    """Поддерживаемые типы моделей"""
    OLLAMA = "ollama"
    OPENAI = "openai"
    GIGACHAT = "gigachat"
    ANTHROPIC = "anthropic"

class LLMFactory:
    """Фабрика для создания экземпляров различных LLM моделей"""
    
    DEFAULT_MODELS = {
        ModelType.OLLAMA: "llama3.2",
        ModelType.OPENAI: "gpt-4",
        ModelType.GIGACHAT: "GigaChat:latest",
        ModelType.ANTHROPIC: "claude-3.5"
    }

    @staticmethod
    def create_llm(
        model_type: Union[ModelType, str],
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        streaming: bool = True,
        **kwargs
    ) -> BaseLanguageModel:
        """
        Создает экземпляр LLM модели указанного типа.
        
        Args:
            model_type: Тип модели (OLLAMA, OPENAI, GIAGACHAT, ANTHROPIC)
            model_name: Название конкретной модели (опционально)
            temperature: Температура генерации
            streaming: Использовать ли потоковый вывод
            **kwargs: Дополнительные параметры для конкретной модели
            
        Returns:
            BaseLanguageModel: Экземпляр модели
        """
        if isinstance(model_type, str):
            try:
                model_type = ModelType(model_type.lower())
            except ValueError:
                raise ValueError(f"Unsupported model type: {model_type}")

        # Настройка callback manager для streaming
        callbacks = [StreamingStdOutCallbackHandler()] if streaming else []
        callback_manager = CallbackManager(callbacks)

        # Если model_name не указан, используем значение по умолчанию
        if not model_name:
            model_name = LLMFactory.DEFAULT_MODELS[model_type]

        try:
            if model_type == ModelType.OLLAMA:
                return OllamaLLM(
                    model=model_name,
                    callback_manager=callback_manager,
                    temperature=temperature,
                    base_url="http://localhost:11434",  # Явное указание URL
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
                    model_name=model_name,
                    temperature=temperature,
                    streaming=streaming,
                    anthropic_api_key=api_key,
                    **kwargs
                )
            
            elif model_type == ModelType.GIGACHAT:
                credentials = os.getenv("GIGACHAT_CREDENTIALS")
                if not credentials:
                    raise ValueError("GIGACHAT_CREDENTIALS not found in environment variables")
                
                # Создаем экземпляр GigaChat
                return GigaChat(
                    credentials=credentials,
                    temperature=temperature,
                    streaming=streaming,
                    verify_ssl_certs=False,  # Часто требуется для работы с GigaChat
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
    ) -> None:
        """
        Добавляет модель в менеджер.
        
        Args:
            model_type: Тип модели
            model_name: Название модели (опционально)
            alias: Псевдоним для модели (опционально)
            make_default: Сделать ли модель моделью по умолчанию
            **kwargs: Дополнительные параметры для модели
        """
        model = LLMFactory.create_llm(model_type, model_name, **kwargs)
        
        # Если alias не указан, используем комбинацию типа и названия модели
        if not alias:
            alias = f"{model_type.value}_{model_name or LLMFactory.DEFAULT_MODELS[ModelType(model_type)]}"
            
        self.models[alias] = model
        
        if make_default or not self.default_model:
            self.default_model = alias

    def get_model(self, alias: Optional[str] = None) -> BaseLanguageModel:
        """
        Получает модель по псевдониму.
        
        Args:
            alias: Псевдоним модели (опционально)
            
        Returns:
            BaseLanguageModel: Запрошенная модель
        """
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
    """
    Инициализирует одиночную модель LLM (для обратной совместимости).
    
    Args:
        model_type: Тип модели
        model_name: Название модели (опционально)
        **kwargs: Дополнительные параметры
        
    Returns:
        BaseLanguageModel: Инициализированная модель
    """
    return LLMFactory.create_llm(model_type, model_name, **kwargs)
