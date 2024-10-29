# service/prompts.py

from collections.abc import Mapping, Sequence
from enum import Enum
import logging
from dataclasses import dataclass
from narr_mod import get_narrative_structure

logger = logging.getLogger(__name__)

class NarrativeStructureType(Enum):
    HERO_JOURNEY = "hero_journey"
    THREE_ACT = "three_act"
    FOUR_ACT = "four_act"
    FIVE_ACT = "five_act"
    
@dataclass
class PromptConfig:
    structure_type: NarrativeStructureType
    aspects: Sequence[str]
    evaluation_criteria: Sequence[str]
    improvement_focus: Sequence[str]

class PromptGenerator:
    """Генератор промптов для различных типов нарративных структур"""
    
    def __init__(self):
        self.configs: Mapping[NarrativeStructureType, PromptConfig] = {
            NarrativeStructureType.HERO_JOURNEY: PromptConfig(
                structure_type=NarrativeStructureType.HERO_JOURNEY,
                aspects=[
                    "character_development",
                    "mythological_elements",
                    "transformation_arc",
                    "mentor_relationship"
                ],
                evaluation_criteria=[
                    "adherence_to_stages",
                    "emotional_impact",
                    "symbolic_depth",
                    "character_growth"
                ],
                improvement_focus=[
                    "stage_transitions",
                    "emotional_resonance",
                    "mythological_symbolism",
                    "character_arc_completion"
                ]
            ),
            # ... остальные конфигурации ...
        }

    def get_evaluation_prompt(
        self,
        structure_name: str,
        formatted_structure: Mapping[str, Sequence[str]],
        focus_aspects: Sequence[str] | None = None
    ) -> str:
        """Генерирует промпт для оценки нарративной структуры."""
        try:
            narrative_structure = get_narrative_structure(structure_name)
            return narrative_structure.get_prompt()
            
        except ValueError:
            try:
                structure_type = NarrativeStructureType(structure_name)
                return self._generate_legacy_prompt(structure_type, formatted_structure, focus_aspects)
            except ValueError:
                logger.error(f"Unknown structure name: {structure_name}")
                raise ValueError(f"Unsupported narrative structure type: {structure_name}")

    def _generate_legacy_prompt(
        self,
        structure_type: NarrativeStructureType,
        formatted_structure: Mapping[str, Sequence[str]],
        focus_aspects: Sequence[str] | None = None
    ) -> str:
        """Генерирует промпт для устаревших типов структур."""
        config = self.configs.get(structure_type)
        if not config:
            raise ValueError(f"Configuration not found for structure type: {structure_type}")

        # ... остальная логика метода ...

    def add_structure_config(self, config: PromptConfig) -> None:
        """Добавляет новую конфигурацию структуры."""
        self.configs[config.structure_type] = config

# Глобальный экземпляр
prompt_generator = PromptGenerator()

# Функции для обратной совместимости
def get_evaluation_prompt(
    structure_name: str,
    formatted_structure: Mapping[str, Sequence[str]]
) -> str:
    return prompt_generator.get_evaluation_prompt(structure_name, formatted_structure)

def hero_journey_prompt(structure: Mapping[str, Sequence[str]]) -> str:
    return prompt_generator.get_evaluation_prompt(
        NarrativeStructureType.HERO_JOURNEY.value,
        structure
    )

def three_act_prompt(structure: Mapping[str, Sequence[str]]) -> str:
    return prompt_generator.get_evaluation_prompt(
        NarrativeStructureType.THREE_ACT.value,
        structure
    )

def four_act_prompt(structure: Mapping[str, Sequence[str]]) -> str:
    return prompt_generator.get_evaluation_prompt(
        NarrativeStructureType.FOUR_ACT.value,
        structure
    )
