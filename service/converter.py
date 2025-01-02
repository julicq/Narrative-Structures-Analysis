# service/converter.py

from dataclasses import dataclass
from typing import Dict, List, Callable, Optional, Any
from enum import Enum
import math
import logging

logger = logging.getLogger(__name__)
class StoryStructure(Enum):
    FOUR_ACT = "four_act"
    THREE_ACT = "three_act"
    HERO_JOURNEY = "hero_journey"
    FIELD_PARADIGM = "field_paradigm"
    HARMON_STORY_CIRCLE = "harmon_story_circle"
    GULINO_SEQUENCE = "gulino_sequence"
    SOTH_STORY_STRUCTURE = "soth_story_structure"
    VOGLER_HERO_JOURNEY = "vogler_hero_journey"
    WATTS_EIGHT_POINT_ARC = "watts_eight_point_arc"
    MONOMYTH = "monomyth"

@dataclass
class StorySegment:
    name: str
    proportion: float  # доля от общего количества предложений
    min_sentences: int = 1  # минимальное количество предложений

@dataclass
class StructureDefinition:
    name: str
    segments: List[StorySegment]
    description: str
    
    def analyze(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализирует структуру повествования.
        
        Args:
            structure: Структура для анализа
            
        Returns:
            Dict[str, Any]: Результаты анализа
        """
        analysis = {
            "segments": {},
            "proportions": {},
            "completeness": 0.0,
            "balance": 0.0
        }
        
        # Анализируем каждый сегмент
        total_content = 0
        for segment in self.segments:
            segment_content = structure.get(segment.name, "")
            content_length = len(segment_content.split()) if segment_content else 0
            analysis["segments"][segment.name] = {
                "content_length": content_length,
                "expected_proportion": segment.proportion,
                "completeness": 1.0 if content_length > 0 else 0.0,
                "balance": 0.0  # Initialize balance for each segment
            }
            total_content += content_length
        
        # Вычисляем реальные пропорции и баланс
        if total_content > 0:
            for segment_name, segment_data in analysis["segments"].items():
                actual_proportion = segment_data["content_length"] / total_content
                expected_proportion = segment_data["expected_proportion"]
                analysis["proportions"][segment_name] = actual_proportion
                
                # Оцениваем баланс сегмента
                proportion_diff = abs(actual_proportion - expected_proportion)
                segment_data["balance"] = max(0.0, 1.0 - proportion_diff)
        
        # Вычисляем общие метрики
        analysis["completeness"] = sum(s["completeness"] for s in analysis["segments"].values()) / len(self.segments)
        analysis["balance"] = sum(s["balance"] for s in analysis["segments"].values()) / len(self.segments)
        
        return analysis
    
    def visualize(self, analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Создает визуализацию анализа структуры.
        
        Args:
            analysis: Результаты анализа
            
        Returns:
            Optional[Dict[str, Any]]: Данные для визуализации
        """
        try:
            visualization = {
                "structure_name": self.name,
                "segments": [],
                "metrics": {
                    "completeness": analysis.get("completeness", 0.0),
                    "balance": analysis.get("balance", 0.0)
                }
            }
            
            # Формируем данные для каждого сегмента
            for segment in self.segments:
                segment_data = analysis.get("segments", {}).get(segment.name, {})
                visualization["segments"].append({
                    "name": segment.name,
                    "expected_proportion": segment.proportion,
                    "actual_proportion": analysis.get("proportions", {}).get(segment.name, 0.0),
                    "completeness": segment_data.get("completeness", 0.0),
                    "balance": segment_data.get("balance", 0.0)
                })
            
            return visualization
            
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            return None
    
    def get_prompt(self) -> str:
        """
        Возвращает промпт для анализа структуры.
        
        Returns:
            str: Промпт для анализа
        """
        return f"""Analyze the following text using {self.name} structure.
        Structure segments: {', '.join(segment.name for segment in self.segments)}
        Description: {self.description}
        
        Focus on:
        1. How well the text follows the expected structure
        2. Balance between segments
        3. Completeness of each segment
        4. Overall narrative flow
        
        Please provide a concise analysis."""
    
    @property
    def display_name(self) -> str:
        """
        Возвращает отображаемое имя структуры.
        
        Returns:
            str: Отображаемое имя
        """
        return self.name

class StoryStructureConverter:
    """Конвертер для различных структур повествования."""

    STRUCTURE_DEFINITIONS = {
        StoryStructure.FOUR_ACT: StructureDefinition(
            "Four Act Structure",
            [
                StorySegment("act1_setup", 0.25),
                StorySegment("act2_complication", 0.25),
                StorySegment("act3_development", 0.25),
                StorySegment("act4_resolution", 0.25)
            ],
            "Classical four-act structure with equal parts for setup, complication, development, and resolution"
        ),
        
        StoryStructure.THREE_ACT: StructureDefinition(
            "Three Act Structure",
            [
                StorySegment("act1_setup", 0.25),
                StorySegment("act2_confrontation", 0.5),
                StorySegment("act3_resolution", 0.25)
            ],
            "Traditional three-act structure with setup, confrontation, and resolution"
        ),
        
        StoryStructure.HERO_JOURNEY: StructureDefinition(
            "Hero's Journey",
            [
                StorySegment("ordinary_world", 0.1),
                StorySegment("call_to_adventure", 0.1),
                StorySegment("refusal_of_the_call", 0.1),
                StorySegment("meeting_the_mentor", 0.1),
                StorySegment("crossing_the_threshold", 0.1),
                StorySegment("tests_allies_enemies", 0.15),
                StorySegment("approach", 0.1),
                StorySegment("ordeal", 0.1),
                StorySegment("reward", 0.05),
                StorySegment("road_back", 0.05),
                StorySegment("resurrection", 0.1),
                StorySegment("return_with_elixir", 0.05)
            ],
            "Campbell's Hero's Journey structure with twelve stages"
        ),
        
        StoryStructure.FIELD_PARADIGM: StructureDefinition(
            "Field's Paradigm",
            [
                StorySegment("setup", 0.25),
                StorySegment("confrontation", 0.5),
                StorySegment("resolution", 0.25)
            ],
            "Syd Field's paradigm for screenplay structure"
        ),
        
        StoryStructure.HARMON_STORY_CIRCLE: StructureDefinition(
            "Harmon Story Circle",
            [
                StorySegment("you", 0.125),
                StorySegment("need", 0.125),
                StorySegment("go", 0.125),
                StorySegment("search", 0.125),
                StorySegment("find", 0.125),
                StorySegment("take", 0.125),
                StorySegment("return", 0.125),
                StorySegment("change", 0.125)
            ],
            "Dan Harmon's Story Circle with eight equal segments"
        ),
        
        StoryStructure.GULINO_SEQUENCE: StructureDefinition(
            "Gulino Sequence Approach",
            [
                StorySegment("introduction", 0.05),
                StorySegment("stating_goal", 0.05),
                StorySegment("presenting_mystery", 0.05),
                StorySegment("heightening_curiosity", 0.1),
                StorySegment("reaction_to_event", 0.1),
                StorySegment("emergence_of_problem", 0.1),
                StorySegment("first_attempt", 0.1),
                StorySegment("solution_probability", 0.1),
                StorySegment("new_characters_subplots", 0.1),
                StorySegment("rethinking_tension", 0.05),
                StorySegment("raised_stakes", 0.05),
                StorySegment("accelerated_pace", 0.05),
                StorySegment("all_is_lost", 0.05),
                StorySegment("final_resolution", 0.05)
            ],
            "Paul Gulino's Sequence Approach with fourteen segments"
        ),
        
        StoryStructure.SOTH_STORY_STRUCTURE: StructureDefinition(
            "Chris Soth Story Structure",
            [
                StorySegment("hero_world_call", 0.11),
                StorySegment("meeting_antagonist", 0.11),
                StorySegment("hero_locked_in", 0.11),
                StorySegment("first_attempts", 0.11),
                StorySegment("moving_forward", 0.11),
                StorySegment("eye_opening_trial", 0.11),
                StorySegment("new_plan", 0.11),
                StorySegment("final_battle", 0.11),
                StorySegment("new_equilibrium", 0.12)
            ],
            "Chris Soth story structure"
        ),
        
        StoryStructure.VOGLER_HERO_JOURNEY: StructureDefinition(
            "Vogler's Hero Journey",
            [
                StorySegment("ordinary_world", 0.08),
                StorySegment("call_to_adventure", 0.08),
                StorySegment("refusal_of_call", 0.08),
                StorySegment("meeting_with_mentor", 0.08),
                StorySegment("crossing_threshold", 0.08),
                StorySegment("tests_allies_enemies", 0.1),
                StorySegment("approach_inmost_cave", 0.1),
                StorySegment("ordeal", 0.1),
                StorySegment("reward", 0.08),
                StorySegment("road_back", 0.08),
                StorySegment("resurrection", 0.08),
                StorySegment("return_with_elixir", 0.06)
            ],
            "Christopher Vogler's adaptation of Campbell's Hero's Journey"
        ),
        
        StoryStructure.WATTS_EIGHT_POINT_ARC: StructureDefinition(
            "Watts Eight Point Arc",
            [
                StorySegment("stasis", 0.1),
                StorySegment("trigger", 0.1),
                StorySegment("the_quest", 0.15),
                StorySegment("surprise", 0.15),
                StorySegment("critical_choice", 0.15),
                StorySegment("climax", 0.15),
                StorySegment("reversal", 0.1),
                StorySegment("resolution", 0.1)
            ],
            "Nigel Watts' Eight-Point Arc structure"
        ),

        StoryStructure.MONOMYTH: StructureDefinition(
        "Campbell's Monomyth",
        [
            StorySegment("ordinary_world", 0.06),
            StorySegment("call_to_adventure", 0.06),
            StorySegment("refusal_of_call", 0.06),
            StorySegment("meeting_mentor", 0.06),
            StorySegment("crossing_threshold", 0.06),
            StorySegment("belly_of_whale", 0.06),
            StorySegment("road_of_trials", 0.08),
            StorySegment("goddess_meeting", 0.06),
            StorySegment("woman_temptress", 0.06),
            StorySegment("atonement_father", 0.06),
            StorySegment("apotheosis", 0.08),
            StorySegment("ultimate_boon", 0.06),
            StorySegment("refusal_return", 0.06),
            StorySegment("magic_flight", 0.06),
            StorySegment("rescue_without", 0.06),
            StorySegment("crossing_return", 0.06),
            StorySegment("master_two_worlds", 0.06),
            StorySegment("freedom_to_live", 0.06)
        ],
        "Joseph Campbell's complete Monomyth structure with seventeen stages of the hero's journey"
        ),
    }

    @classmethod
    def convert_to_format(cls, structure: Dict, structure_name: str) -> Dict[str, str]:
        """
        Конвертирует исходную структуру в указанный формат.
        
        Args:
            structure: Исходная структура с предложениями
            structure_name: Название целевой структуры
            
        Returns:
            Dict[str, str]: Сконвертированная структура
        
        Raises:
            ValueError: Если структура неизвестна или некорректна
        """
        try:
            story_structure = StoryStructure(structure_name)
        except ValueError:
            raise ValueError(f"Unknown structure name: {structure_name}")

        if not cls.validate_structure(structure):
            return {"error": "Invalid or empty structure"}

        structure_def = cls.STRUCTURE_DEFINITIONS.get(story_structure)
        if not structure_def:
            raise ValueError(f"Structure definition not found for: {structure_name}")

        return cls._convert_using_definition(structure["sentences"], structure_def)

    @staticmethod
    def _convert_using_definition(
        sentences: List[str],
        structure_def: StructureDefinition
    ) -> Dict[str, str]:
        """
        Конвертирует предложения согласно определению структуры.
        
        Args:
            sentences: Список предложений
            structure_def: Определение структуры
            
        Returns:
            Dict[str, str]: Сконвертированная структура
        """
        total_sentences = len(sentences)
        result = {}
        current_index = 0

        for segment in structure_def.segments:
            # Вычисляем количество предложений для сегмента
            segment_size = max(
                segment.min_sentences,
                math.floor(total_sentences * segment.proportion)
            )
            
            # Убеждаемся, что не выходим за пределы массива
            if current_index + segment_size > total_sentences:
                segment_size = total_sentences - current_index

            # Добавляем сегмент в результат
            result[segment.name] = ' '.join(
                sentences[current_index:current_index + segment_size]
            )
            
            current_index += segment_size

        return result

    @classmethod
    def get_structure_info(cls, structure_name: str) -> Optional[Dict]:
        """
        Возвращает информацию о структуре повествования.
        
        Args:
            structure_name: Название структуры
            
        Returns:
            Optional[Dict]: Информация о структуре или None
        """
        try:
            story_structure = StoryStructure(structure_name)
            structure_def = cls.STRUCTURE_DEFINITIONS.get(story_structure)
            if structure_def:
                return {
                    "name": structure_def.name,
                    "description": structure_def.description,
                    "segments": [
                        {
                            "name": segment.name,
                            "proportion": segment.proportion,
                            "min_sentences": segment.min_sentences
                        }
                        for segment in structure_def.segments
                    ]
                }
        except ValueError:
            pass
        return None

    @classmethod
    def validate_structure(cls, structure: Dict) -> bool:
        """
        Проверяет корректность структуры.
        
        Args:
            structure: Структура для проверки
            
        Returns:
            bool: True если структура корректна
        """
        if not structure or "sentences" not in structure:
            return False
        
        if not isinstance(structure["sentences"], list):
            return False
        
        if not all(isinstance(s, str) for s in structure["sentences"]):
            return False
        
        return True

    @classmethod
    def get_available_structures(cls) -> List[Dict]:
        """
        Возвращает список доступных структур с их описаниями.
        
        Returns:
            List[Dict]: Список структур с описаниями
        """
        return [
            {
                "name": structure.value,
                "display_name": structure_def.name,
                "description": structure_def.description,
                "segment_count": len(structure_def.segments)
            }
            for structure, structure_def in cls.STRUCTURE_DEFINITIONS.items()
        ]
    
    def get_structure(self, structure_name: Optional[str] = None) -> Optional[StructureDefinition]:
        """
        Возвращает определение структуры по её имени.
        
        Args:
            structure_name: Название структуры (опционально)
            
        Returns:
            Optional[StructureDefinition]: Определение структуры или None если структура не найдена
        """
        try:
            if structure_name is None:
                # Возвращаем структуру по умолчанию (three_act)
                return self.STRUCTURE_DEFINITIONS[StoryStructure.THREE_ACT]
                
            # Пробуем получить структуру по имени
            story_structure = StoryStructure(structure_name.lower())
            return self.STRUCTURE_DEFINITIONS.get(story_structure)
            
        except ValueError:
            # Если структура не найдена в enum, пробуем найти по маппингу
            structure_mapping = {
                'three': StoryStructure.THREE_ACT,
                'three-act': StoryStructure.THREE_ACT,
                'three act': StoryStructure.THREE_ACT,
                'four': StoryStructure.FOUR_ACT,
                'four-act': StoryStructure.FOUR_ACT,
                'four act': StoryStructure.FOUR_ACT,
                'hero': StoryStructure.HERO_JOURNEY,
                "hero's journey": StoryStructure.HERO_JOURNEY,
                'heros journey': StoryStructure.HERO_JOURNEY,
                'vogler': StoryStructure.VOGLER_HERO_JOURNEY,
                'campbell': StoryStructure.MONOMYTH,
                'monomyth': StoryStructure.MONOMYTH,
                'field': StoryStructure.FIELD_PARADIGM,
                'paradigm': StoryStructure.FIELD_PARADIGM,
                'harmon': StoryStructure.HARMON_STORY_CIRCLE,
                'story circle': StoryStructure.HARMON_STORY_CIRCLE,
                'gulino': StoryStructure.GULINO_SEQUENCE,
                'sequence': StoryStructure.GULINO_SEQUENCE,
                'soth': StoryStructure.SOTH_STORY_STRUCTURE,
                'watts': StoryStructure.WATTS_EIGHT_POINT_ARC,
                'eight point': StoryStructure.WATTS_EIGHT_POINT_ARC,
                'eight-point': StoryStructure.WATTS_EIGHT_POINT_ARC
            }
            
            # Ищем ближайшее совпадение в маппинге
            if structure_name:
                structure_name_lower = structure_name.lower()
                for key, value in structure_mapping.items():
                    if key in structure_name_lower:
                        return self.STRUCTURE_DEFINITIONS.get(value)
            
            # Если структура не найдена, возвращаем None
            return None
        
    @classmethod
    def get_default_structure(cls) -> StructureDefinition:
        """
        Возвращает структуру по умолчанию (three_act).
        
        Returns:
            StructureDefinition: Структура по умолчанию
        """
        return cls.STRUCTURE_DEFINITIONS[StoryStructure.THREE_ACT]

    @classmethod
    def get_structure_by_enum(cls, structure_type: StoryStructure) -> Optional[StructureDefinition]:
        """
        Возвращает определение структуры по enum.
        
        Args:
            structure_type: Тип структуры из enum StoryStructure
            
        Returns:
            Optional[StructureDefinition]: Определение структуры или None
        """
        return cls.STRUCTURE_DEFINITIONS.get(structure_type)

    def format_structure(self, structure_def: StructureDefinition) -> Dict[str, Any]:
        """
        Форматирует определение структуры в словарь.
        
        Args:
            structure_def: Определение структуры
            
        Returns:
            Dict[str, Any]: Отформатированная структура
        """
        return {
            "name": structure_def.name,
            "description": structure_def.description,
            "segments": [
                {
                    "name": segment.name,
                    "proportion": segment.proportion,
                    "min_sentences": segment.min_sentences
                }
                for segment in structure_def.segments
            ]
        }

def convert_to_format(structure: dict, structure_name: str) -> dict[str, str]:
    """
    Обёртка для обратной совместимости.
    """
    return StoryStructureConverter.convert_to_format(structure, structure_name)