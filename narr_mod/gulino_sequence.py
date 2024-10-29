# narr_mod/gulino_sequence.py

from dataclasses import dataclass
from typing import List, Tuple, Final, ClassVar
from narr_mod import NarrativeStructure

@dataclass
class SequenceElement:
    name: str
    css_class: str
    height: int  # высота в процентах
    act: str
    description: str

@dataclass
class Act:
    name: str
    description: str
    width: int  # ширина в процентах

class GulinoSequence(NarrativeStructure):
    """Implementation of Paul Gulino's Sequence Approach narrative structure."""

    # Константы для актов
    ACT_BEGINNING: Final[str] = "Beginning"
    ACT_MIDDLE: Final[str] = "Middle"
    ACT_END: Final[str] = "End"

    # Определение элементов последовательности
    SEQUENCE_ELEMENTS: ClassVar[List[SequenceElement]] = [
        SequenceElement("Введение", "introduction", 40, ACT_BEGINNING,
                       "Setup of the story world and characters"),
        SequenceElement("Указание цели", "stating-goal", 60, ACT_BEGINNING,
                       "Clear statement of protagonist's goal"),
        SequenceElement("Загадка", "mystery", 60, ACT_BEGINNING,
                       "Introduction of the central mystery"),
        SequenceElement("Усиление любопытства", "heighten-curiosity", 60, ACT_BEGINNING,
                       "Building viewer engagement"),
        SequenceElement("Реакция на событие", "event-reaction", 60, ACT_BEGINNING,
                       "Character response to inciting incident"),
        SequenceElement("Возникновение проблемы", "problem-emergence", 60, ACT_BEGINNING,
                       "Major problem emerges"),
        SequenceElement("Первая попытка", "first-attempt", 80, ACT_MIDDLE,
                       "Hero's initial attempt to solve the problem"),
        SequenceElement("Вероятность решения", "solution-probability", 80, ACT_MIDDLE,
                       "Possibility of solution emerges"),
        SequenceElement("Новые герои и подсюжеты", "new-characters-subplots", 80, ACT_MIDDLE,
                       "Introduction of new elements"),
        SequenceElement("Переосмысление напряжения", "tension-rethinking", 80, ACT_MIDDLE,
                       "Calm before the storm"),
        SequenceElement("Повышенные ставки", "raised-stakes", 100, ACT_END,
                       "Stakes are raised"),
        SequenceElement("Ускоренный темп", "accelerated-pace", 100, ACT_END,
                       "Pace quickens"),
        SequenceElement("Момент «все потеряно»", "all-is-lost", 100, ACT_END,
                       "Darkest moment"),
        SequenceElement("Финальное решение", "final-resolution", 40, ACT_END,
                       "Resolution with twist")
    ]

    # Определение актов
    ACTS: ClassVar[List[Act]] = [
        Act("Акт 1", "Начало", 30),
        Act("Акт 2 - Акт 3", "Середина", 40),
        Act("Акт 4", "Конец", 30)
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

    def name(self) -> str:
        return "Consistent Approach (Paul Gulino)"

    def analyze(self, formatted_structure: dict) -> dict:
        """
        Analyze the narrative structure according to Gulino's Sequence Approach.
        
        Args:
            formatted_structure: Dictionary containing the narrative structure
            
        Returns:
            dict: Analysis results with sequence elements evaluation
        """
        analysis = {
            "acts": {
                self.ACT_BEGINNING: [],
                self.ACT_MIDDLE: [],
                self.ACT_END: []
            },
            "elements": {element.name: {
                "presence": self._evaluate_element_presence(element, formatted_structure),
                "description": element.description
            } for element in self.SEQUENCE_ELEMENTS},
            "overall_evaluation": self._evaluate_overall_structure(formatted_structure)
        }
        
        return {**formatted_structure, "analysis": analysis}

    def _evaluate_element_presence(self, element: SequenceElement, structure: dict) -> bool:
        """Evaluate presence of sequence element in the structure."""
        # Здесь можно добавить более сложную логику оценки
        return True

    def _evaluate_overall_structure(self, structure: dict) -> dict:
        """Evaluate overall narrative structure."""
        return {
            "balance": "Balanced structure",
            "pacing": "Good pacing",
            "suggestions": []
        }

    def get_prompt(self) -> str:
        """Generate the analysis prompt for Gulino's Sequence Approach."""
        prompt_parts = [
            "Analyze the following narrative structure based on Paul Gulino's Sequence Approach:\n"
        ]

        for act in self.ACTS:
            prompt_parts.append(f"\n{act.name} - {act.description}:")
            elements = [elem for elem in self.SEQUENCE_ELEMENTS if elem.act == act.name]
            for i, elem in enumerate(elements, 1):
                prompt_parts.append(f"{i}. {elem.name} - {elem.description}")

        return "\n".join(prompt_parts)

    def visualize(self, analysis_result: dict) -> str:
        """
        Generate HTML visualization of the Gulino Sequence.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            str: HTML representation of the sequence
        """
        html_parts = [
            "<h1>Последовательный подход (Пол Гулино)</h1>",
            "<div class='gulino-approach'>",
            "<div class='timeline'>"
        ]

        # Добавляем элементы последовательности
        for i, element in enumerate(self.SEQUENCE_ELEMENTS, 1):
            html_parts.extend([
                f"<div class='element {element.css_class}' style='height: {element.height}%'>",
                f"<div class='element-number'>{i}</div>",
                f"<div class='element-name'>{element.name}</div>",
                "</div>"
            ])

        html_parts.append("</div><div class='acts'>")

        # Добавляем акты
        for act in self.ACTS:
            html_parts.append(
                f"<div class='act' style='width: {act.width}%'>{act.name}<br>{act.description}</div>"
            )

        # Закрываем контейнеры и добавляем стили
        html_parts.extend([
            "</div>",
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)
