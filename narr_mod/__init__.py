# narr_mod/__init__.py

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

    def double_check_prompt(self) -> str:
        return """
        Before finalizing your analysis, please double-check your classification:

        1. Review the key characteristics of both 3-act and 4-act structures:
           - 3-act: Setup, Confrontation, Resolution
           - 4-act: Setup, Complication, Development, Resolution

        2. Carefully examine the narrative for these specific elements:
           - Is there a clear midpoint that could serve as a division between acts 2 and 3 in a 4-act structure?
           - Does the story have a distinct complication phase separate from the main confrontation?
           - Is the development of the conflict spread across multiple acts or concentrated in one?

        3. Consider the pacing and balance:
           - Does the story feel evenly divided into three parts, or does it have a more complex structure that fits better into four parts?

        4. Look for any potential misclassification:
           - If you initially classified it as 3-act, could it actually be a 4-act structure with a subtle act division?
           - If you initially classified it as 4-act, could it be a 3-act structure with a particularly detailed middle act?

        5. Make your final decision:
           - Based on this review, confirm whether your initial classification is correct or if it needs to be changed.
           - Provide a brief explanation for your final decision, highlighting the key factors that led to this conclusion.

        Remember, the goal is accuracy, not sticking to your initial assessment. It's okay to change your classification if the evidence supports it.
        """

def get_narrative_structure(structure_name):
    try:
        module = import_module(f"narr_mod.{structure_name.lower()}")
        class_name = ''.join(word.capitalize() for word in structure_name.split('_'))
        return getattr(module, class_name)
    except (ImportError, AttributeError):
        raise ValueError(f"Unknown structure name: {structure_name}")
