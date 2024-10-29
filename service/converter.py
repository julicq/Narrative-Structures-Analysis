# service/converter.py

from dataclasses import dataclass
from typing import Dict, List, Callable, Optional
from enum import Enum
import math

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

def convert_to_format(structure: dict, structure_name: str) -> dict[str, str]:
    """
    Обёртка для обратной совместимости.
    """
    return StoryStructureConverter.convert_to_format(structure, structure_name)
