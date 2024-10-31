# narr_mod/gulino_sequence.py

from dataclasses import dataclass
from typing import List, Tuple, Final, ClassVar
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

@dataclass
class SequenceElement:
    name: str
    name_en: str
    css_class: str
    height: int  # высота в процентах
    act: str
    description: str
    description_en: str

@dataclass
class Act:
    name: str
    name_en: str
    description: str
    description_en: str
    width: int  # ширина в процентах

class GulinoSequence(NarrativeStructure):
    """Implementation of Paul Gulino's Sequence Approach narrative structure."""

    @property
    def structure_type(self) -> StructureType:
        return StructureType.GULINO_SEQUENCE

    # Константы для актов
    ACT_BEGINNING: Final[str] = "Beginning"
    ACT_MIDDLE: Final[str] = "Middle"
    ACT_END: Final[str] = "End"

    # Определение элементов последовательности
    SEQUENCE_ELEMENTS: ClassVar[List[SequenceElement]] = [
        SequenceElement(
            "Введение", "Introduction", "introduction", 40, ACT_BEGINNING,
            "Установка мира истории и персонажей",
            "Setup of the story world and characters"
        ),
        SequenceElement(
            "Указание цели", "Stating Goal", "stating-goal", 60, ACT_BEGINNING,
            "Четкое определение цели протагониста",
            "Clear statement of protagonist's goal"
        ),
        SequenceElement(
            "Загадка", "Mystery", "mystery", 60, ACT_BEGINNING,
            "Введение центральной загадки",
            "Introduction of the central mystery"
        ),
        SequenceElement(
            "Усиление любопытства", "Heighten Curiosity", "heighten-curiosity", 60, ACT_BEGINNING,
            "Повышение вовлеченности зрителя",
            "Building viewer engagement"
        ),
        SequenceElement(
            "Реакция на событие", "Event Reaction", "event-reaction", 60, ACT_BEGINNING,
            "Реакция персонажа на провоцирующее событие",
            "Character response to inciting incident"
        ),
        SequenceElement(
            "Возникновение проблемы", "Problem Emergence", "problem-emergence", 60, ACT_BEGINNING,
            "Появление основной проблемы",
            "Major problem emerges"
        ),
        SequenceElement(
            "Первая попытка", "First Attempt", "first-attempt", 80, ACT_MIDDLE,
            "Первая попытка героя решить проблему",
            "Hero's initial attempt to solve the problem"
        ),
        SequenceElement(
            "Вероятность решения", "Solution Probability", "solution-probability", 80, ACT_MIDDLE,
            "Появление возможного решения",
            "Possibility of solution emerges"
        ),
        SequenceElement(
            "Новые герои и подсюжеты", "New Characters & Subplots", "new-characters-subplots", 80, ACT_MIDDLE,
            "Введение новых элементов",
            "Introduction of new elements"
        ),
        SequenceElement(
            "Переосмысление напряжения", "Tension Rethinking", "tension-rethinking", 80, ACT_MIDDLE,
            "Затишье перед бурей",
            "Calm before the storm"
        ),
        SequenceElement(
            "Повышенные ставки", "Raised Stakes", "raised-stakes", 100, ACT_END,
            "Повышение ставок",
            "Stakes are raised"
        ),
        SequenceElement(
            "Ускоренный темп", "Accelerated Pace", "accelerated-pace", 100, ACT_END,
            "Ускорение темпа",
            "Pace quickens"
        ),
        SequenceElement(
            "Момент «все потеряно»", "All Is Lost", "all-is-lost", 100, ACT_END,
            "Самый темный момент",
            "Darkest moment"
        ),
        SequenceElement(
            "Финальное решение", "Final Resolution", "final-resolution", 40, ACT_END,
            "Развязка с неожиданным поворотом",
            "Resolution with twist"
        )
    ]

    # Определение актов
    ACTS: ClassVar[List[Act]] = [
        Act("Акт 1", "Act 1", "Начало", "Beginning", 30),
        Act("Акт 2 - Акт 3", "Act 2 - Act 3", "Середина", "Middle", 40),
        Act("Акт 4", "Act 4", "Конец", "End", 30)
    ]

    CSS_TEMPLATE: ClassVar[str] = """
    .gulino-approach {
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        font-family: Arial, sans-serif;
    }
    .timeline {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        height: 300px;
        margin-bottom: 20px;
    }
    .element {
        width: 7%;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .element-number {
        background-color: #e74c3c;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 5px;
    }
    .element-name {
        transform: rotate(-45deg);
        white-space: nowrap;
        font-size: 11px;
        margin-top: 10px;
    }
    .acts {
        display: flex;
        justify-content: space-between;
    }
    .act {
        text-align: center;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 5px;
    }
    """

    def analyze(self, text: str, lang: str = 'en') -> AnalysisResult:
        """
        Analyze the narrative structure according to Gulino's Sequence Approach.
        
        Args:
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            AnalysisResult: Analysis results with sequence elements evaluation
        """
        structure = {
            "acts": {
                self.ACT_BEGINNING: [],
                self.ACT_MIDDLE: [],
                self.ACT_END: []
            },
            "elements": {
                (element.name if lang == 'ru' else element.name_en): {
                    "presence": self._evaluate_element_presence(element, text),
                    "description": element.description if lang == 'ru' else element.description_en
                } for element in self.SEQUENCE_ELEMENTS
            },
            "overall_evaluation": self._evaluate_overall_structure(text, lang)
        }
        
        metadata = AnalysisMetadata(
            model_name="gpt-4",
            model_version="1.0",
            confidence=0.85,
            processing_time=1.0,
            structure_type=self.structure_type,
            display_name=self.display_name
        )
        
        summary = ("Анализ нарративной структуры по методу последовательного подхода Пола Гулино" 
                  if lang == 'ru' else 
                  "Analysis of narrative structure using Gulino's Sequence Approach")
        
        visualization = self.visualize(structure, lang)
        
        return AnalysisResult(
            structure=structure,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )

    def _evaluate_element_presence(self, element: SequenceElement, text: str) -> bool:
        """
        Evaluate presence of sequence element in the text.
        
        Args:
            element: Sequence element to evaluate
            text: Input text to analyze
            
        Returns:
            bool: True if element is present
        """
        # Здесь должна быть реальная логика оценки наличия элемента в тексте
        return True

    def _evaluate_overall_structure(self, text: str, lang: str = 'en') -> dict:
        """
        Evaluate overall narrative structure.
        
        Args:
            text: Input text to analyze
            lang: Language for evaluation ('en' or 'ru')
            
        Returns:
            dict: Evaluation results
        """
        if lang == 'ru':
            return {
                "balance": "Сбалансированная структура",
                "pacing": "Хороший темп",
                "suggestions": []
            }
        return {
            "balance": "Balanced structure",
            "pacing": "Good pacing",
            "suggestions": []
        }

    def get_prompt(self, lang: str = 'en') -> str:
        """
        Generate the analysis prompt for Gulino's Sequence Approach.
        
        Args:
            lang: Language for the prompt ('en' or 'ru')
        """
        if lang == 'ru':
            prompt_parts = [
                "Проанализируйте следующую нарративную структуру на основе последовательного подхода Пола Гулино:\n"
            ]

            for act in self.ACTS:
                prompt_parts.append(f"\n{act.name} - {act.description}:")
                elements = [elem for elem in self.SEQUENCE_ELEMENTS if elem.act == act.name]
                for i, elem in enumerate(elements, 1):
                    prompt_parts.append(f"{i}. {elem.name} - {elem.description}")
        else:
            prompt_parts = [
                "Analyze the following narrative structure based on Paul Gulino's Sequence Approach:\n"
            ]

            for act in self.ACTS:
                prompt_parts.append(f"\n{act.name_en} - {act.description_en}:")
                elements = [elem for elem in self.SEQUENCE_ELEMENTS if elem.act == act.name]
                for i, elem in enumerate(elements, 1):
                    prompt_parts.append(f"{i}. {elem.name_en} - {elem.description_en}")

        return "\n".join(prompt_parts)

    def visualize(self, analysis_result: dict, lang: str = 'en') -> str:
        """
        Generate HTML visualization of the Gulino Sequence.
        
        Args:
            analysis_result: Dictionary containing analysis results
            lang: Language for visualization ('en' or 'ru')
            
        Returns:
            str: HTML representation of the sequence
        """
        title = ("Последовательный подход (Пол Гулино)" if lang == 'ru' 
                else "Sequence Approach (Paul Gulino)")
        
        html_parts = [
            f"<h1>{title}</h1>",
            "<div class='gulino-approach'>",
            "<div class='timeline'>"
        ]

        for i, element in enumerate(self.SEQUENCE_ELEMENTS, 1):
            element_name = element.name if lang == 'ru' else element.name_en
            html_parts.extend([
                f"<div class='element {element.css_class}' style='height: {element.height}%'>",
                f"<div class='element-number'>{i}</div>",
                f"<div class='element-name'>{element_name}</div>",
                "</div>"
            ])

        html_parts.append("</div><div class='acts'>")

        for act in self.ACTS:
            act_name = act.name if lang == 'ru' else act.name_en
            act_desc = act.description if lang == 'ru' else act.description_en
            html_parts.append(
                f"<div class='act' style='width: {act.width}%'>{act_name}<br>{act_desc}</div>"
            )

        html_parts.extend([
            "</div>",
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)
