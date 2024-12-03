"""
Service module initialization.
Provides access to LLM initialization and narrative evaluation functionality.
"""

from logging import getLogger
from typing import Optional, Dict, Any
from shared.config import settings, ModelType

logger = getLogger(__name__)

try:
    from .llm import initialize_llm, LLMFactory
except ImportError as e:
    logger.error(f"Failed to import LLM module: {e}")
    initialize_llm = None
    LLMFactory = None

try:
    from .evaluator import NarrativeEvaluator
except ImportError as e:
    logger.error(f"Failed to import NarrativeEvaluator: {e}")
    NarrativeEvaluator = None

__all__ = ['initialize_llm', 'NarrativeEvaluator', 'get_service_status', 'is_service_ready']

def initialize_default_model() -> Optional[Any]:
    """
    Инициализирует модель по умолчанию из конфигурации.
    
    Returns:
        Optional[Any]: Инициализированная модель или None в случае ошибки
    """
    try:
        if not initialize_llm:
            logger.error("LLM initialization function not available")
            return None
            
        active_model = settings.active_model
        if isinstance(active_model, str):
            active_model = ModelType(active_model.lower())
            
        model = initialize_llm(
            model_type=active_model,
            model_name=getattr(settings, f"{active_model}_model_name", None)
        )
        logger.info(f"Successfully initialized default model: {active_model}")
        return model
    except Exception as e:
        logger.error(f"Failed to initialize default model: {e}")
        return None

def is_service_ready() -> bool:
    """
    Проверяет готовность сервиса к работе.
    
    Returns:
        bool: True если все компоненты успешно загружены, False в противном случае
    """
    components_ready = all([
        initialize_llm is not None,
        NarrativeEvaluator is not None,
        LLMFactory is not None
    ])

    if not components_ready:
        logger.warning("Not all service components are initialized")
        return False
        
    # Проверяем доступность выбранной модели
    try:
        if LLMFactory and settings.active_model:
            model_available = LLMFactory.check_availability(settings.active_model)
            if not model_available:
                logger.warning(f"Selected model {settings.active_model} is not available")
                return False
    except Exception as e:
        logger.error(f"Error checking model availability: {e}")
        return False
        
    return True

def get_service_status() -> Dict[str, Any]:
    """
    Возвращает подробный статус компонентов сервиса.
    
    Returns:
        Dict[str, Any]: Словарь со статусом каждого компонента
    """
    status = {
        'components': {
            'llm_initialized': initialize_llm is not None,
            'evaluator_initialized': NarrativeEvaluator is not None,
            'factory_initialized': LLMFactory is not None
        },
        'configuration': {
            'active_model': str(settings.active_model),
            'model_name': getattr(settings, f"{settings.active_model}_model_name", None),
            'debug_mode': settings.debug
        }
    }
    
    # Добавляем информацию о доступности модели
    try:
        if LLMFactory and settings.active_model:
            status['model_availability'] = {
                'active_model_available': LLMFactory.check_availability(settings.active_model),
                'fallback_available': bool(LLMFactory.FALLBACK_CHAIN.get(settings.active_model))
            }
    except Exception as e:
        status['model_availability'] = {
            'error': str(e)
        }
    
    return status

# Проверка при импорте модуля
if not is_service_ready():
    logger.warning(
        "Some service components failed to initialize. "
        "Check logs for details or run get_service_status() for more information."
    )
