from abc import ABC, abstractmethod

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
