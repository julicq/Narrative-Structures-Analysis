# service/__init__.py

"""
Service module initialization.
Provides access to LLM initialization and narrative evaluation functionality.
"""

from logging import getLogger

logger = getLogger(__name__)

try:
    from .llm import initialize_llm
except ImportError as e:
    logger.error(f"Failed to import LLM module: {e}")
    initialize_llm = None

try:
    from .evaluator import NarrativeEvaluator
except ImportError as e:
    logger.error(f"Failed to import NarrativeEvaluator: {e}")
    NarrativeEvaluator = None

__all__ = ['initialize_llm', 'NarrativeEvaluator']

def is_service_ready():
    """
    Проверяет готовность сервиса к работе.
    
    Returns:
        True если все компоненты успешно загружены, False в противном случае
    """
    return all([initialize_llm is not None, NarrativeEvaluator is not None])

def get_service_status():
    """
    Возвращает статус компонентов сервиса.
    
    Returns:
        Словарь со статусом каждого компонента
    """
    return {
        'llm_initialized': initialize_llm is not None,
        'evaluator_initialized': NarrativeEvaluator is not None
    }

# Проверка при импорте модуля
if not is_service_ready():
    logger.warning("Some service components failed to initialize. Check logs for details.")
