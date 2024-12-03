# shared/models_api.py

from collections.abc import Mapping
from gigachat import GigaChat
from langchain_community.chat_models import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
import base64
import logging
from shared.config import settings, ModelType

logger = logging.getLogger(__name__)

class ModelAPI:
    def __init__(self):
        logger.info(f"Initializing ModelAPI with {settings.active_model}")
        self.model = self._initialize_model()
        self.prompt = self._create_prompt()
        logger.info("ModelAPI initialization completed")

    def _initialize_model(self) -> GigaChat | ChatOpenAI:
        """Инициализация выбранной модели"""
        try:
            if settings.active_model == ModelType.GIGACHAT:
                if not settings.gigachat_token:
                    raise ValueError("GigaChat credentials not found")
                return GigaChat(
                    credentials=settings.gigachat_token,
                    verify_ssl_certs=settings.gigachat_verify_ssl
                )
            
            elif settings.active_model == ModelType.OPENAI:
                if not settings.openai_api_key:
                    raise ValueError("OpenAI API key not found")
                return ChatOpenAI(
                    model_name=settings.openai_model_name,
                    temperature=0.7,
                    api_key=settings.openai_api_key
                )
            
            elif settings.active_model == ModelType.OLLAMA:
                return OllamaLLM(
                    model=settings.ollama_model_name, 
                    temperature=0.7, 
                    callback_manager=None, 
                    base_url=settings.ollama_base_url or "http://localhost:11434"
                )
                
            else:
                raise ValueError(f"Unsupported model type: {settings.active_model}")

        except Exception as e:
            print(f"Error initializing model {settings.active_model}: {e}")
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
            if settings.active_model == ModelType.OLLAMA:
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
                'model_info': str(settings.active_model)
            }

    def get_model_info(self) -> dict:
        """Получение информации о текущей модели"""
        return {
            'model_type': str(settings.active_model),
            'model_name': getattr(settings, f"{settings.active_model}_model_name", None),
            'base_url': settings.ollama_base_url if settings.active_model == ModelType.OLLAMA else None
        }

# Глобальный экземпляр API
model_api = ModelAPI()
