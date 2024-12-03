# narr_mod/field_paradigm.py

from dataclasses import dataclass
from typing import Final, ClassVar, List, Tuple, Dict
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

@dataclass
class ParadigmElement:
    name: str
    name_en: str  # Добавляем английское название
    css_class: str
    height: int  # высота в процентах
    act: str

class FieldParadigm(NarrativeStructure):
    """Implementation of Syd Field's Paradigm narrative structure."""

    @property
    def structure_type(self) -> StructureType:
        return StructureType.FIELD_PARADIGM

    CSS_TEMPLATE = """
        .field-paradigm {
            /* CSS стили для визуализации структуры Field's Paradigm */
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            padding: 20px;
        }
        /* Добавьте другие необходимые стили */
        """

    # Константы для актов
    ACT_SETUP: Final[str] = "Setup"
    ACT_CONFRONTATION: Final[str] = "Confrontation"
    ACT_RESOLUTION: Final[str] = "Resolution"

    # Словарь актов на разных языках
    ACTS_DICT: ClassVar[Dict[str, Dict[str, str]]] = {
        'ru': {
            ACT_SETUP: "Завязка",
            ACT_CONFRONTATION: "Противостояние",
            ACT_RESOLUTION: "Развязка"
        },
        'en': {
            ACT_SETUP: "Setup",
            ACT_CONFRONTATION: "Confrontation",
            ACT_RESOLUTION: "Resolution"
        }
    }

    # Определение элементов парадигмы
    ELEMENTS: ClassVar[List[ParadigmElement]] = [
        ParadigmElement(
            name="Провоцирующее событие",
            name_en="Inciting Incident",
            css_class="inciting-incident",
            height=30,
            act=ACT_SETUP
        ),
        ParadigmElement(
            name="Сюжетный поворот 1",
            name_en="Plot Point 1",
            css_class="plot-point-1",
            height=80,
            act=ACT_SETUP
        ),
        ParadigmElement(
            name="Точка фокусировки 1",
            name_en="Pinch 1",
            css_class="pinch-1",
            height=50,
            act=ACT_CONFRONTATION
        ),
        ParadigmElement(
            name="Мидпоинт",
            name_en="Midpoint",
            css_class="midpoint",
            height=60,
            act=ACT_CONFRONTATION
        ),
        ParadigmElement(
            name="Точка фокусировки 2",
            name_en="Pinch 2",
            css_class="pinch-2",
            height=50,
            act=ACT_CONFRONTATION
        ),
        ParadigmElement(
            name="Сюжетный поворот 2",
            name_en="Plot Point 2",
            css_class="plot-point-2",
            height=80,
            act=ACT_CONFRONTATION
        ),
        ParadigmElement(
            name="Кульминация",
            name_en="Climax",
            css_class="climax",
            height=100,
            act=ACT_RESOLUTION
        ),
        ParadigmElement(
            name="Развязка",
            name_en="Resolution",
            css_class="resolution",
            height=30,
            act=ACT_RESOLUTION
        ),
    ]

    ACTS: ClassVar[Dict[str, List[Tuple[str, str, int]]]] = {
        'ru': [
            ("Акт 1", "Завязка", 30),
            ("Акт 2 - Акт 3", "Противостояние", 40),
            ("Акт 4", "Развязка", 30),
        ],
        'en': [
            ("Act 1", "Setup", 30),
            ("Act 2 - Act 3", "Confrontation", 40),
            ("Act 4", "Resolution", 30),
        ]
    }

    # Двуязычные шаблоны промптов
    PROMPT_TEMPLATES: ClassVar[Dict[str, str]] = {
        'en': """
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
        """,
        
        'ru': """
        Проанализируйте следующую нарративную структуру на основе "Парадигмы" Сида Филда:

        Акт 1 - Начало (Завязка):
        1. Провоцирующее событие
        2. Сюжетный поворот 1

        Акт 2 - Середина (Противостояние):
        3. Точка фокусировки 1
        4. Мидпоинт
        5. Точка фокусировки 2
        6. Сюжетный поворот 2

        Акт 3 - Конец (Развязка):
        7. Кульминация
        8. Развязка

        Критерии оценки:
        1. Насколько эффективно Провоцирующее событие задает историю?
        2. Является ли Сюжетный поворот 1 сильной точкой перехода к Акту 2?
        3. Насколько хорошо Точки фокусировки 1 и 2 поддерживают напряжение?
        4. Эффективно ли Мидпоинт меняет направление или повышает ставки?
        5. Достаточно ли значим Сюжетный поворот 2 для перехода к финальному акту?
        6. Насколько удовлетворительна и логична Кульминация?
        7. Обеспечивает ли Развязка удовлетворительное завершение?

        Пожалуйста, проанализируйте темп и баланс между актами, отмечая недостаточно развитые или чрезмерно акцентированные элементы.
        """
    }

    def get_prompt(self, lang: str = 'en') -> str:
        """
        Generate the analysis prompt for Field's Paradigm in specified language.
        
        Args:
            lang: Language code ('en' or 'ru')
            
        Returns:
            str: Prompt text in specified language
        """
        if lang not in ['en', 'ru']:
            lang = 'en'  # fallback to English
        return self.PROMPT_TEMPLATES[lang]

    def analyze(self, text: str, lang: str = 'en') -> AnalysisResult:
        """
        Analyze the narrative structure according to Field's Paradigm.
        
        Args:
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            AnalysisResult: Analysis results
        """
        structure = {
            "acts": {
                self.ACTS_DICT[lang][self.ACT_SETUP]: {},
                self.ACTS_DICT[lang][self.ACT_CONFRONTATION]: {},
                self.ACTS_DICT[lang][self.ACT_RESOLUTION]: {}
            },
            "elements": {
                element.name if lang == 'ru' else element.name_en: {} 
                for element in self.ELEMENTS
            },
            "overall_evaluation": {}
        }
        
        metadata = AnalysisMetadata(
            model_name="gpt-4",
            model_version="1.0",
            confidence=0.85,
            processing_time=1.0,
            structure_type=self.structure_type,
            display_name=self.display_name
        )
        
        summary = ("Анализ нарративной структуры по методу Сида Филда" 
                  if lang == 'ru' else 
                  "Analysis of narrative structure using Syd Field's Paradigm")
        
        visualization = self.visualize(structure, lang)
        
        return AnalysisResult(
            structure=structure,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )

    def visualize(self, analysis_result: dict, lang: str = 'en') -> str:
        """
        Generate HTML visualization of the Field's Paradigm.
        
        Args:
            analysis_result: Dictionary containing analysis results
            lang: Language for visualization ('en' or 'ru')
            
        Returns:
            str: HTML representation of the paradigm
        """
        title = "Парадигма (Сид Филд)" if lang == 'ru' else "Paradigm (Syd Field)"
    
        html_parts = [
            f"<h1>{title}</h1>",
            "<div class='field-paradigm'>",
            "<div class='timeline'>"
        ]

        for element in self.ELEMENTS:
            element_name = element.name if lang == 'ru' else element.name_en
            html_parts.extend([
                f"<div class='element {element.css_class}' style='height: {element.height}%'>",
                f"<div class='element-name'>{element_name}</div>",
                "</div>"
            ])

        html_parts.append("</div><div class='acts'>")

        for act_name, act_desc, width in self.ACTS[lang]:
            html_parts.append(
                f"<div class='act' style='width: {width}%'>{act_name}<br>{act_desc}</div>"
            )

        html_parts.extend([
            "</div>",
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)
