# narr_mod/field_paradigm.py

from dataclasses import dataclass
from typing import Final, ClassVar, List, Tuple
from narr_mod import NarrativeStructure

@dataclass
class ParadigmElement:
    name: str
    css_class: str
    height: int  # высота в процентах
    act: str

class FieldParadigm(NarrativeStructure):
    """Implementation of Syd Field's Paradigm narrative structure."""

    # Константы для актов
    ACT_SETUP: Final[str] = "Setup"
    ACT_CONFRONTATION: Final[str] = "Confrontation"
    ACT_RESOLUTION: Final[str] = "Resolution"

    # Определение элементов парадигмы
    ELEMENTS: ClassVar[List[ParadigmElement]] = [
        ParadigmElement("Провоцирующее событие", "inciting-incident", 30, ACT_SETUP),
        ParadigmElement("Сюжетный поворот 1", "plot-point-1", 80, ACT_SETUP),
        ParadigmElement("Точка фокусировки 1", "pinch-1", 50, ACT_CONFRONTATION),
        ParadigmElement("Мидпоинт", "midpoint", 60, ACT_CONFRONTATION),
        ParadigmElement("Точка фокусировки 2", "pinch-2", 50, ACT_CONFRONTATION),
        ParadigmElement("Сюжетный поворот 2", "plot-point-2", 80, ACT_CONFRONTATION),
        ParadigmElement("Кульминация", "climax", 100, ACT_RESOLUTION),
        ParadigmElement("Развязка", "resolution", 30, ACT_RESOLUTION),
    ]

    ACTS: ClassVar[List[Tuple[str, str, int]]] = [
        ("Акт 1", "Завязка", 30),
        ("Акт 2 - Акт 3", "Противостояние", 40),
        ("Акт 4", "Развязка", 30),
    ]

    PROMPT_TEMPLATE: ClassVar[str] = """
    Analyze the following narrative structure based on Syd Field's "Paradigm":

    Act 1 - Beginning (Setup):
    1. Inciting Incident
    2. Plot Point 1

    Act 2 - Middle (Confrontation):
    3. Pinch 1
    4. Midpoint
    5. Pinch 2
    6. Plot Point 2

    Act 3 - End (Resolution):
    7. Climax
    8. Resolution

    Evaluation Criteria:
    1. How effectively does the Inciting Incident set up the story?
    2. Is Plot Point 1 a strong turning point that propels the story into Act 2?
    3. How well do Pinch 1 and Pinch 2 maintain tension?
    4. Does the Midpoint effectively shift the direction or raise the stakes?
    5. Is Plot Point 2 impactful enough to transition into the final act?
    6. How satisfying and logical is the Climax?
    7. Does the Resolution provide a satisfying conclusion?

    Please analyze pacing and balance between acts, noting any underdeveloped or overemphasized elements.
    """

    CSS_TEMPLATE: ClassVar[str] = """
    .field-paradigm {
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        font-family: Arial, sans-serif;
    }
    .timeline {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        height: 200px;
        margin-bottom: 20px;
    }
    .element {
        width: 10%;
        text-align: center;
    }
    .element-name {
        transform: rotate(-45deg);
        white-space: nowrap;
        font-size: 12px;
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
        return "Paradigm (Sid Field)"

    def analyze(self, formatted_structure: dict) -> dict:
        """
        Analyze the narrative structure according to Field's Paradigm.
        
        Args:
            formatted_structure: Dictionary containing the narrative structure
            
        Returns:
            dict: Analysis results with elements and acts evaluation
        """
        analysis = {
            "acts": {
                self.ACT_SETUP: {},
                self.ACT_CONFRONTATION: {},
                self.ACT_RESOLUTION: {}
            },
            "elements": {element.name: {} for element in self.ELEMENTS},
            "overall_evaluation": {}
        }
        
        return {**formatted_structure, "analysis": analysis}

    def get_prompt(self) -> str:
        """Generate the analysis prompt for the Field's Paradigm."""
        return self.PROMPT_TEMPLATE

    def visualize(self, analysis_result: dict) -> str:
        """
        Generate HTML visualization of the Field's Paradigm.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            str: HTML representation of the paradigm
        """
        html_parts = [
            "<h1>Парадигма (Сид Филд)</h1>",
            "<div class='field-paradigm'>",
            "<div class='timeline'>"
        ]

        # Добавляем элементы
        for element in self.ELEMENTS:
            html_parts.extend([
                f"<div class='element {element.css_class}' style='height: {element.height}%'>",
                f"<div class='element-name'>{element.name}</div>",
                "</div>"
            ])

        html_parts.append("</div><div class='acts'>")

        # Добавляем акты
        for act_name, act_desc, width in self.ACTS:
            html_parts.append(
                f"<div class='act' style='width: {width}%'>{act_name}<br>{act_desc}</div>"
            )

        # Закрываем контейнеры и добавляем стили
        html_parts.extend([
            "</div>",
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)
