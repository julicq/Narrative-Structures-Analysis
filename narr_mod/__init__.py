# narr_mod/__init__.py

from abc import ABC, abstractmethod
from importlib import import_module
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict

class StructureType(str, Enum):
    """Поддерживаемые типы нарративных структур"""
    WATTS_EIGHT_POINT = "watts_eight_point_arc"
    VOGLER_HERO_JOURNEY = "vogler_hero_journey"
    FOUR_ACT = "four_act"
    FIELD_PARADIGM = "field_paradigm"
    THREE_ACT = "three_act"
    MONOMYTH = "monomyth"
    SOTH_STRUCTURE = "soth_story_structure"
    HARMON_CIRCLE = "harmon_story_circle"
    GULINO_SEQUENCE = "gulino_sequence"
    AUTO_DETECT = "auto_detect"

    @classmethod
    def get_display_name(cls, value: str) -> str:
        """Получить человекочитаемое название структуры"""
        display_names = {
            cls.WATTS_EIGHT_POINT.value: "Eight Point Arc (Nigel Watts)",
            cls.VOGLER_HERO_JOURNEY.value: "Hero's journey (Chris Vogler)",
            cls.FOUR_ACT.value: "Four-Act Structure",
            cls.FIELD_PARADIGM.value: "Paradigm (Sid Field)",
            cls.THREE_ACT.value: "Three-Act Structure",
            cls.MONOMYTH.value: "The Monomyth (Joseph Campbell)",
            cls.SOTH_STRUCTURE.value: "The Structure of Story (Chris Soth)",
            cls.HARMON_CIRCLE.value: "Story Circle (Dan Harmon)",
            cls.GULINO_SEQUENCE.value: "Consistent Approach (Paul Gulino)",
            cls.AUTO_DETECT.value: "Auto Detect"
        }
        return display_names.get(value, value)

class AnalysisMetadata(BaseModel):
    """Метаданные анализа"""
    model_config = ConfigDict(protected_namespaces=())  # Добавляем эту строку
    
    model_name: str = Field(..., description="Name of the model used")
    model_version: str = Field(..., description="Model version")
    confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time: float = Field(..., gt=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    structure_type: StructureType
    display_name: str = Field(...)

    @field_validator('display_name')
    @classmethod
    def set_display_name(cls, v: str, info) -> str:
        if 'structure_type' in info.data:
            return StructureType.get_display_name(info.data['structure_type'])
        return v

class AnalysisResult(BaseModel):
    """Результат анализа нарративной структуры"""
    structure: Dict[str, Any] = Field(..., description="Structured analysis result")
    summary: str = Field(..., description="Text summary of analysis")
    visualization: Optional[str] = Field(None, description="HTML visualization")
    metadata: AnalysisMetadata

class NarrativeStructure(ABC):
    """Базовый класс для анализа нарративных структур"""
    
    @property
    @abstractmethod
    def structure_type(self) -> StructureType:
        """Возвращает тип нарративной структуры"""
        pass

    @property
    def display_name(self) -> str:
        """Возвращает человекочитаемое название структуры"""
        return StructureType.get_display_name(self.structure_type.value)

    @abstractmethod
    def analyze(self, text: str) -> AnalysisResult:
        """
        Анализирует текст и возвращает результат анализа
        
        Args:
            text: Входной текст для анализа
            
        Returns:
            AnalysisResult: Результат анализа
        """
        pass

    @abstractmethod
    def get_prompt(self) -> str:
        """Возвращает промпт для LLM для данной структуры"""
        pass

    @abstractmethod
    def visualize(self, analysis_result: Dict[str, Any]) -> str:
        """
        Создает HTML визуализацию результата анализа
        
        Args:
            analysis_result: Результат анализа для визуализации
            
        Returns:
            str: HTML строка с визуализацией
        """
        pass

    def double_check_prompt(self) -> str:
        """Промпт для перепроверки классификации"""
        return """
        Before finalizing your analysis, please double-check your classification:
        [существующий текст промпта]
        """

def get_narrative_structure(structure_type: StructureType) -> NarrativeStructure:
    """
    Фабричный метод для создания анализатора нарративной структуры
    
    Args:
        structure_type: Тип нарративной структуры
        
    Returns:
        NarrativeStructure: Экземпляр анализатора
        
    Raises:
        ValueError: Если указан неизвестный тип структуры
    """
    if structure_type == StructureType.AUTO_DETECT:
        # Здесь можно добавить логику автоопределения структуры
        raise NotImplementedError("Auto detection not implemented yet")
        
    try:
        module = import_module(f"narr_mod.{structure_type.value}")
        class_name = ''.join(word.capitalize() for word in structure_type.value.split('_'))
        structure_class = getattr(module, class_name)
        return structure_class()
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Unknown structure type: {structure_type}") from e
