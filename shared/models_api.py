# shared/models_api.py

from collections.abc import Mapping
from gigachat import GigaChat
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Anthropic
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
import base64
import logging
from .config import Config, ModelType

logger = logging.getLogger(__name__)

class ModelAPI:
    def __init__(self):
        logger.info(f"Initializing ModelAPI with {Config.ACTIVE_MODEL.value}")
        self.model = self._initialize_model()
        self.prompt = self._create_prompt()
        logger.info("ModelAPI initialization completed")

    def _initialize_model(self) -> GigaChat | ChatOpenAI | Anthropic:
        """Инициализация выбранной модели"""
        try:
            if Config.ACTIVE_MODEL == ModelType.GIGACHAT:
                if not Config.GIGACHAT_CREDENTIALS:
                    raise ValueError("GigaChat credentials not found")
                return GigaChat(
                    credentials=Config.GIGACHAT_CREDENTIALS,
                    verify_ssl_certs=False
                )
            
            elif Config.ACTIVE_MODEL == ModelType.OPENAI:
                if not Config.OPENAI_API_KEY:
                    raise ValueError("OpenAI API key not found")
                return ChatOpenAI(
                    model_name=Config.OPENAI_MODEL_NAME,
                    temperature=0.7,
                    api_key=Config.OPENAI_API_KEY
                )
            
            elif Config.ACTIVE_MODEL == ModelType.ANTHROPIC:
                if not Config.ANTHROPIC_API_KEY:
                    raise ValueError("Anthropic API key not found")
                return Anthropic(
                    model=Config.ANTHROPIC_MODEL_NAME,
                    api_key=Config.ANTHROPIC_API_KEY
                )
            
            elif Config.ACTIVE_MODEL == ModelType.OLLAMA:
                return OllamaLLM(
                    model=Config.OLLAMA_MODEL_NAME, 
                    temperature=0.7, 
                    callback_manager=None, 
                    base_url=Config.OLLAMA_BASE_URL or "http://localhost:11434"
                )
                
            else:
                raise ValueError(f"Unsupported model type: {Config.ACTIVE_MODEL}")

        except Exception as e:
            print(f"Error initializing model {Config.ACTIVE_MODEL}: {e}")
            raise

    def _create_prompt(self) -> PromptTemplate:
        """Создание шаблона промпта"""
        return PromptTemplate(
            input_variables=["text", "structure_type"],
            template="""
            Проанализируй следующий текст с точки зрения нарративной структуры {structure_type}.
            
            Текст:
            {text}
            
            Предоставь анализ в следующем формате:
            1. Основные элементы структуры
            2. Ключевые моменты повествования
            3. Рекомендации по улучшению
            4. Соответствие выбранной структуре (в процентах)
            """
        )

    def analyze_text(self, text: str, structure_type: str) -> Mapping[str, str]:
        """Синхронный анализ текста"""
        try:
            logger.info(f"Starting analysis with structure type: {structure_type}")
            logger.info(f"Text length: {len(text)} characters")

            # Формируем промпт
            formatted_prompt = self.prompt.format(
                text=text,
                structure_type=structure_type
            )

            # Для Ollama используем прямой вызов
            if Config.ACTIVE_MODEL == ModelType.OLLAMA:
                logger.info("Using direct Ollama call")
                result = self.model.invoke(formatted_prompt)
                analysis_text = str(result)
            else:
                # Для других моделей используем RunnableSequence
                chain = RunnableSequence.from_components([
                    self.prompt,
                    self.model
                ])
                result = chain.invoke({
                    "text": text,
                    "structure_type": structure_type
                })
                analysis_text = result.content if hasattr(result, 'content') else str(result)
            
            logger.info("Analysis completed successfully")
            
            return {
                'status': 'success',
                'analysis': analysis_text,
                'model_info': self.get_model_info()
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': f"Error during analysis: {str(e)}",
                'model_info': f"{Config.ACTIVE_MODEL.value}"
            }

        
    def get_model_info(self) -> dict:
        """Получение информации о текущей модели"""
        return {
            'model_type': Config.ACTIVE_MODEL.value,
            'model_name': getattr(Config, f"{Config.ACTIVE_MODEL.value}_MODEL_NAME", None),
            'base_url': getattr(Config, "OLLAMA_BASE_URL", None) if Config.ACTIVE_MODEL == ModelType.OLLAMA else None
        }

# Глобальный экземпляр API
model_api = ModelAPI()
