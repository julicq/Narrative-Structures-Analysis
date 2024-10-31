# narr_mod/soth_story_structure.py

from dataclasses import dataclass
from typing import List, Dict, Final, ClassVar
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

@dataclass
class StoryElement:
    number: int
    name: str
    name_en: str
    css_class: str
    height: int  # высота в процентах
    act: str
    description: str
    description_en: str
    analysis_points: List[str]
    analysis_points_en: List[str]

@dataclass
class Act:
    name: str
    name_en: str
    description: str
    description_en: str
    width: int  # ширина в процентах
    elements: List[int]  # номера элементов в этом акте

class SothStoryStructure(NarrativeStructure):
    """Implementation of Chris Soth's Mini-Movie Method story structure."""

    @property
    def structure_type(self) -> StructureType:
        return StructureType.SOTH_STRUCTURE

    # Константы для актов
    ACT_BEGINNING: Final[str] = "Beginning"
    ACT_MIDDLE: Final[str] = "Middle"
    ACT_END: Final[str] = "End"

    # Определение элементов структуры
    STORY_ELEMENTS: ClassVar[List[StoryElement]] = [
        StoryElement(
            1, "Мир героя: Зов приключений", "Hero's World: Call to Adventure",
            "call-to-adventure", 30, ACT_BEGINNING,
            "Установка мира истории и призыв к приключениям", 
            "Hero's World: Call to Adventure",
            ["установка мира", "ясность призыва", "начальное состояние героя"],
            ["world establishment", "call clarity", "hero's initial state"]
        ),
        StoryElement(
            2, "Встреча с антагонистом", "Meeting the Antagonist",
            "meet-antagonist", 50, ACT_BEGINNING,
            "Первое столкновение с антагонистом",
            "Meeting the Antagonist",
            ["представление антагониста", "установка конфликта", "определение ставок"],
            ["antagonist introduction", "conflict establishment", "stakes definition"]
        ),
        StoryElement(
            3, "Герой «заперт» вместе с антагонистом", "Hero is Locked In",
            "locked-in", 50, ACT_BEGINNING,
            "Герой оказывается в безвыходной ситуации",
            "Lazy Hero: Hero is locked in",
            ["эскалация ситуации", "уровень вовлеченности", "точка невозврата"],
            ["situation escalation", "commitment level", "point of no return"]
        ),
        StoryElement(
            4, "Первые попытки", "First Attempts",
            "first-attempts", 70, ACT_MIDDLE,
            "Обычные методы не работают",
            "First Attempts: Usual methods don't work",
            ["подход к решению проблем", "начальные неудачи", "кривая обучения"],
            ["problem-solving approach", "initial failures", "learning curve"]
        ),
        StoryElement(
            5, "Большой дерзкий план проваливается", "Bold Plan Fails",
            "bold-plan-fails", 70, ACT_MIDDLE,
            "Амбициозный план терпит неудачу",
            "Moving Forward: Big bold plan fails",
            ["амбициозность плана", "выявление недостатков", "серьезность последствий"],
            ["plan ambition", "flaw revelation", "consequence severity"]
        ),
        StoryElement(
            6, "Испытание, открывающее герою глаза", "Eye-Opening Trial",
            "eye-opening-trial", 70, ACT_MIDDLE,
            "Герой решает измениться",
            "Eye-Opening Trial: Hero decides to change",
            ["влияние осознания", "рост персонажа", "принятие решения"],
            ["realization impact", "character growth", "decision making"]
        ),
        StoryElement(
            7, "Новый план проваливается", "New Plan Fails",
            "new-plan-fails", 70, ACT_MIDDLE,
            "Впечатляющий провал",
            "New Plan: Spectacular failure",
            ["исполнение плана", "масштаб неудачи", "потеря надежды"],
            ["plan execution", "failure magnitude", "hope loss"]
        ),
        StoryElement(
            8, "Победа в финальной битве", "Victory in Final Battle",
            "final-battle", 100, ACT_END,
            "Решающее сражение",
            "Victory in the Final Battle",
            ["трансформация персонажа", "разрешение конфликта", "достоверность победы"],
            ["character transformation", "conflict resolution", "victory credibility"]
        ),
        StoryElement(
            9, "Новое равновесие", "New Equilibrium",
            "new-equilibrium", 30, ACT_END,
            "Достижение нового баланса",
            "New equilibrium achieved",
            ["изменение мира", "рост персонажа", "удовлетворительность развязки"],
            ["world change", "character growth", "resolution satisfaction"]
        )
    ]

    # Определение актов
    ACTS: ClassVar[List[Act]] = [
        Act("Акт 1", "Act 1", "Начало", "Beginning", 25, [1, 2, 3]),
        Act("Акт 2-3", "Act 2-3", "Середина", "Middle", 50, [4, 5, 6, 7]),
        Act("Акт 4", "Act 4", "Конец", "End", 25, [8, 9])
    ]

    CSS_TEMPLATE: ClassVar[str] = """
        .soth-structure {
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        .timeline {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            height: 250px;
            margin-bottom: 20px;
        }
        .element {
            width: 10%;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: all 0.3s ease;
        }
        .element:hover {
            transform: translateY(-10px);
        }
        .element-number {
            background-color: #3498db;
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
            font-size: 12px;
            margin-top: 10px;
        }
        .acts {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        .act {
            text-align: center;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        .act:hover {
            background-color: #e0e0e0;
            transform: scale(1.05);
        }
    """

    def analyze(self, text: str, lang: str = 'en') -> AnalysisResult:
        """
        Analyze the narrative structure according to Soth's Mini-Movie Method.
        
        Args:
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            AnalysisResult: Analysis results with element evaluation
        """
        structure = {
            "elements": {
                (element.name if lang == 'ru' else element.name_en): 
                self._analyze_element(element, text, lang)
                for element in self.STORY_ELEMENTS
            },
            "acts": {
                (act.name if lang == 'ru' else act.name_en): 
                self._analyze_act(act, text, lang)
                for act in self.ACTS
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
        
        summary = ("Анализ нарративной структуры по методу мини-фильмов Криса Сота" 
                  if lang == 'ru' else 
                  "Analysis of narrative structure using Soth's Mini-Movie Method")
        
        visualization = self.visualize(structure, lang)
        
        return AnalysisResult(
            structure=structure,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )

    def _analyze_element(self, element: StoryElement, text: str, lang: str = 'en') -> dict:
        """
        Analyze a single element of the story structure.
        
        Args:
            element: Story element to analyze
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            dict: Analysis results for the element
        """
        return {
            "presence": True,
            "strength": "средний" if lang == 'ru' else "medium",
            "analysis_points": (
                element.analysis_points if lang == 'ru' 
                else element.analysis_points_en
            ),
            "suggestions": []
        }

    def _analyze_act(self, act: Act, text: str, lang: str = 'en') -> dict:
        """
        Analyze an entire act of the story.
        
        Args:
            act: Act to analyze
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            dict: Analysis results for the act
        """
        if lang == 'ru':
            return {
                "баланс": "хорошо_сбалансирован",
                "темп": "хороший",
                "элементы": act.elements,
                "предложения": []
            }
        return {
            "balance": "well_balanced",
            "pacing": "good",
            "elements": act.elements,
            "suggestions": []
        }

    def _evaluate_overall_structure(self, text: str, lang: str = 'en') -> dict:
        """
        Evaluate the overall story structure.
        
        Args:
            text: Input text to analyze
            lang: Language for evaluation ('en' or 'ru')
            
        Returns:
            dict: Overall evaluation results
        """
        if lang == 'ru':
            return {
                "соответствие_структуре": "сильное",
                "темп": "сбалансированный",
                "предложения": []
            }
        return {
            "structure_adherence": "strong",
            "pacing": "balanced",
            "suggestions": []
        }

    def visualize(self, analysis_result: dict, lang: str = 'en') -> str:
        """
        Generate HTML visualization of the story structure.
        
        Args:
            analysis_result: Dictionary containing analysis results
            lang: Language for visualization ('en' or 'ru')
            
        Returns:
            str: HTML representation of the structure
        """
        title = ("Структура истории (Крис Сот)" if lang == 'ru' 
                else "Story Structure (Chris Soth)")
        
        html_parts = [
            f"<h1>{title}</h1>",
            "<div class='soth-structure'>",
            "<div class='timeline'>"
        ]

        for element in self.STORY_ELEMENTS:
            element_name = element.name if lang == 'ru' else element.name_en
            html_parts.extend([
                f"<div class='element {element.css_class}' style='height: {element.height}%'>",
                f"<div class='element-number'>{element.number}</div>",
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

    def get_prompt(self, lang: str = 'en') -> str:
        """
        Generate analysis prompt for the story structure.
        
        Args:
            lang: Language for the prompt ('en' or 'ru')
        """
        if lang == 'ru':
            prompt_parts = [
                "Проанализируйте следующую нарративную структуру на основе метода мини-фильмов Криса Сота:\n"
            ]
        else:
            prompt_parts = [
                "Analyze the following narrative structure based on Chris Soth's Mini-Movie Method:\n"
            ]

        current_act = None
        for element in self.STORY_ELEMENTS:
            if element.act != current_act:
                current_act = element.act
                act_text = f"\nАкт - {current_act}:" if lang == 'ru' else f"\nAct - {current_act}:"
                prompt_parts.append(act_text)
            
            element_name = element.name if lang == 'ru' else element.name_en
            element_desc = element.description if lang == 'ru' else element.description_en
            analysis_points = (element.analysis_points if lang == 'ru' 
                             else element.analysis_points_en)
            
            prompt_parts.append(f"{element.number}. {element_name} ({element_desc})")
            points_label = "   Точки анализа: " if lang == 'ru' else "   Analysis points: "
            prompt_parts.append(points_label + ", ".join(analysis_points))

        return "\n".join(prompt_parts)
