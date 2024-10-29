# narr_mod/soth_story_structure.py

from dataclasses import dataclass
from typing import List, Dict, Final, ClassVar
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

@dataclass
class StoryElement:
    number: int
    name: str
    css_class: str
    height: int  # высота в процентах
    act: str
    description: str
    analysis_points: List[str]

@dataclass
class Act:
    name: str
    description: str
    width: int  # ширина в процентах
    elements: List[int]  # номера элементов в этом акте

class SothStoryStructure(NarrativeStructure):
    """Implementation of Chris Soth's Mini-Movie Method story structure."""

    # Добавляем реализацию абстрактного метода structure_type
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
            1, "Мир героя: Зов приключений",
            "call-to-adventure", 30, ACT_BEGINNING,
            "Hero's World: Call to Adventure",
            ["world establishment", "call clarity", "hero's initial state"]
        ),
        StoryElement(
            2, "Встреча с антагонистом",
            "meet-antagonist", 50, ACT_BEGINNING,
            "Meeting the Antagonist",
            ["antagonist introduction", "conflict establishment", "stakes definition"]
        ),
        StoryElement(
            3, "Герой «заперт» вместе с антагонистом",
            "locked-in", 50, ACT_BEGINNING,
            "Lazy Hero: Hero is locked in",
            ["situation escalation", "commitment level", "point of no return"]
        ),
        StoryElement(
            4, "Первые попытки",
            "first-attempts", 70, ACT_MIDDLE,
            "First Attempts: Usual methods don't work",
            ["problem-solving approach", "initial failures", "learning curve"]
        ),
        StoryElement(
            5, "Большой дерзкий план проваливается",
            "bold-plan-fails", 70, ACT_MIDDLE,
            "Moving Forward: Big bold plan fails",
            ["plan ambition", "flaw revelation", "consequence severity"]
        ),
        StoryElement(
            6, "Испытание, открывающее герою глаза",
            "eye-opening-trial", 70, ACT_MIDDLE,
            "Eye-Opening Trial: Hero decides to change",
            ["realization impact", "character growth", "decision making"]
        ),
        StoryElement(
            7, "Новый план проваливается",
            "new-plan-fails", 70, ACT_MIDDLE,
            "New Plan: Spectacular failure",
            ["plan execution", "failure magnitude", "hope loss"]
        ),
        StoryElement(
            8, "Победа в финальной битве",
            "final-battle", 100, ACT_END,
            "Victory in the Final Battle",
            ["character transformation", "conflict resolution", "victory credibility"]
        ),
        StoryElement(
            9, "Новое равновесие",
            "new-equilibrium", 30, ACT_END,
            "New equilibrium achieved",
            ["world change", "character growth", "resolution satisfaction"]
        )
    ]

    # Определение актов
    ACTS: ClassVar[List[Act]] = [
        Act("Акт 1", "Начало", 25, [1, 2, 3]),
        Act("Акт 2-3", "Середина", 50, [4, 5, 6, 7]),
        Act("Акт 4", "Конец", 25, [8, 9])
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

    def analyze(self, text: str) -> AnalysisResult:
        """
        Analyze the narrative structure according to Soth's Mini-Movie Method.
        
        Args:
            text: Input text to analyze
            
        Returns:
            AnalysisResult: Analysis results with element evaluation
        """
        # Анализируем структуру
        structure = {
            "elements": {
                element.name: self._analyze_element(element, text)
                for element in self.STORY_ELEMENTS
            },
            "acts": {
                act.name: self._analyze_act(act, text)
                for act in self.ACTS
            },
            "overall_evaluation": self._evaluate_overall_structure(text)
        }
        
        # Создаем метаданные
        metadata = AnalysisMetadata(
            model_name="gpt-4",
            model_version="1.0",
            confidence=0.85,
            processing_time=1.0,
            structure_type=self.structure_type,
            display_name=self.display_name
        )
        
        # Создаем краткое описание анализа
        summary = "Analysis of narrative structure using Soth's Mini-Movie Method"
        
        # Создаем визуализацию
        visualization = self.visualize(structure)
        
        return AnalysisResult(
            structure=structure,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )

    def _analyze_element(self, element: StoryElement, text: str) -> dict:
        """
        Analyze a single element of the story structure.
        
        Args:
            element: Story element to analyze
            text: Input text to analyze
            
        Returns:
            dict: Analysis results for the element
        """
        return {
            "presence": True,  # В реальной реализации здесь должен быть анализ текста
            "strength": "medium",
            "analysis_points": element.analysis_points,
            "suggestions": []
        }

    def _analyze_act(self, act: Act, text: str) -> dict:
        """
        Analyze an entire act of the story.
        
        Args:
            act: Act to analyze
            text: Input text to analyze
            
        Returns:
            dict: Analysis results for the act
        """
        return {
            "balance": "well_balanced",
            "pacing": "good",
            "elements": act.elements,
            "suggestions": []
        }

    def _evaluate_overall_structure(self, text: str) -> dict:
        """
        Evaluate the overall story structure.
        
        Args:
            text: Input text to analyze
            
        Returns:
            dict: Overall evaluation results
        """
        return {
            "structure_adherence": "strong",
            "pacing": "balanced",
            "suggestions": []
        }

    def visualize(self, analysis_result: dict) -> str:
        """
        Generate HTML visualization of the story structure.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            str: HTML representation of the structure
        """
        html_parts = [
            "<h1>Структура истории (Крис Сот)</h1>",
            "<div class='soth-structure'>",
            "<div class='timeline'>"
        ]

        # Добавляем элементы
        for element in self.STORY_ELEMENTS:
            html_parts.extend([
                f"<div class='element {element.css_class}' style='height: {element.height}%'>",
                f"<div class='element-number'>{element.number}</div>",
                f"<div class='element-name'>{element.name}</div>",
                "</div>"
            ])

        html_parts.append("</div><div class='acts'>")

        # Добавляем акты
        for act in self.ACTS:
            html_parts.append(
                f"<div class='act' style='width: {act.width}%'>{act.name}<br>{act.description}</div>"
            )

        html_parts.extend([
            "</div>",
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)

    def get_prompt(self) -> str:
        """Generate analysis prompt for the story structure."""
        prompt_parts = [
            "Analyze the following narrative structure based on Chris Soth's Mini-Movie Method:\n"
        ]

        current_act = None
        for element in self.STORY_ELEMENTS:
            if element.act != current_act:
                current_act = element.act
                prompt_parts.append(f"\nAct - {current_act}:")
            
            prompt_parts.append(f"{element.number}. {element.name} ({element.description})")
            prompt_parts.append("   Analysis points: " + ", ".join(element.analysis_points))

        return "\n".join(prompt_parts)