# naarr_mod/__init__.py

from abc import ABC, abstractmethod
from importlib import import_module

class NarrativeStructure(ABC):
    @abstractmethod
    def name(self) -> str:
        """Возвращает название нарративной структуры"""
        pass

    @abstractmethod
    def analyze(self, formatted_structure: dict) -> dict:
        """Анализирует структуру и возвращает результат анализа"""
        pass

    @abstractmethod
    def get_prompt(self) -> str:
        """Возвращает промпт для LLM для данной структуры"""
        pass

    @abstractmethod
    def visualize(self, analysis_result: dict) -> str:
        """Возвращает HTML для визуализации результата анализа"""
        pass

def get_narrative_structure(structure_name):
    try:
        module = import_module(f"narr_mod.{structure_name.lower()}")
        class_name = ''.join(word.capitalize() for word in structure_name.split('_'))
        return getattr(module, class_name)
    except (ImportError, AttributeError):
        raise ValueError(f"Unknown structure name: {structure_name}")
