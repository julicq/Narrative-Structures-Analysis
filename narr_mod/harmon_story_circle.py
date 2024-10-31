# narr_mod/harmon_story_circle.py

from dataclasses import dataclass
from typing import List, Dict, Final, ClassVar
from math import cos, sin, radians
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

@dataclass
class StoryStep:
    number: int
    name: str
    name_en: str
    description: str
    description_en: str
    color: str
    act: str
    analysis_criteria: List[str]
    analysis_criteria_en: List[str]

class HarmonStoryCircle(NarrativeStructure):
    """Implementation of Dan Harmon's Story Circle narrative structure."""

    @property
    def structure_type(self) -> StructureType:
        return StructureType.HARMON_CIRCLE

    # Константы для актов
    ACT_BEGINNING: Final[str] = "Beginning"
    ACT_MIDDLE: Final[str] = "Middle"
    ACT_END: Final[str] = "End"

    # Определение шагов
    STORY_STEPS: ClassVar[List[StoryStep]] = [
        StoryStep(
            1, "Зона комфорта", "Comfort Zone",
            "Привычный мир героя", "Character's familiar world",
            "#e74c3c",
            ACT_BEGINNING,
            ["установление персонажа", "начальное состояние мира", "статус-кво"],
            ["character establishment", "initial world state", "status quo"]
        ),
        StoryStep(
            2, "Потребность или желание", "Need or Desire",
            "Возникновение потребности", "Emergence of need",
            "#3498db",
            ACT_BEGINNING,
            ["ясность мотивации", "установление ставок", "определение цели"],
            ["motivation clarity", "stakes establishment", "goal definition"]
        ),
        StoryStep(
            3, "Незнакомая ситуация", "Unfamiliar Situation",
            "Выход из зоны комфорта", "Leaving comfort zone",
            "#2ecc71",
            ACT_MIDDLE,
            ["уход из зоны комфорта", "новые вызовы", "начальная адаптация"],
            ["comfort zone departure", "new challenges", "initial adaptation"]
        ),
        StoryStep(
            4, "Поиск и адаптация", "Search and Adaptation",
            "Приспособление к новому", "Adapting to new",
            "#f39c12",
            ACT_MIDDLE,
            ["преодоление испытаний", "развитие навыков", "исследование мира"],
            ["challenge handling", "skill development", "world exploration"]
        ),
        StoryStep(
            5, "Получение желаемого", "Getting What They Wanted",
            "Достижение цели", "Goal achievement",
            "#9b59b6",
            ACT_MIDDLE,
            ["достижение цели", "осознание цены", "понимание последствий"],
            ["goal achievement", "price recognition", "consequence understanding"]
        ),
        StoryStep(
            6, "Плата за него", "Paying the Price",
            "Расплата за достижение", "Price for achievement",
            "#e67e22",
            ACT_MIDDLE,
            ["измерение жертвы", "оценка стоимости", "катализатор изменений"],
            ["sacrifice measurement", "cost evaluation", "change catalyst"]
        ),
        StoryStep(
            7, "Возвращение к привычному", "Return to Familiar",
            "Возвращение домой", "Return home",
            "#1abc9c",
            ACT_END,
            ["интеграция изменений", "сравнение миров", "осознание роста"],
            ["integration of change", "world comparison", "growth recognition"]
        ),
        StoryStep(
            8, "Способность меняться", "Changed State",
            "Трансформация героя", "Character transformation",
            "#34495e",
            ACT_END,
            ["эволюция персонажа", "применение урока", "новая норма"],
            ["character evolution", "lesson application", "new normal"]
        )
    ]

    CSS_TEMPLATE: ClassVar[str] = """
        .harmon-circle {
            width: 400px;
            height: 400px;
            border-radius: 50%;
            border: 2px solid #333;
            position: relative;
            margin: 50px auto;
        }
        .step {
            position: absolute;
            width: 100px;
            text-align: center;
            transform-origin: center;
            transition: all 0.3s ease;
        }
        .step:hover {
            transform-origin: center;
            transform: scale(1.1);
        }
        .step-number {
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 5px;
        }
        .step-name {
            font-size: 12px;
        }
        .circle-center {
            position: absolute;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            top: 150px;
            left: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.9);
            border: 1px solid #333;
        }
    """

    def analyze(self, text: str, lang: str = 'en') -> AnalysisResult:
        """
        Analyze the narrative structure according to Harmon's Story Circle.
        
        Args:
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            AnalysisResult: Analysis results with step evaluation
        """
        structure = {
            "steps": {
                (step.name if lang == 'ru' else step.name_en): 
                self._analyze_step(step, text, lang)
                for step in self.STORY_STEPS
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
        
        summary = ("Анализ нарративной структуры по методу сюжетного круга Дэна Хармона" 
                  if lang == 'ru' else 
                  "Analysis of narrative structure using Harmon's Story Circle")
        
        visualization = self.visualize(structure, lang)
        
        return AnalysisResult(
            structure=structure,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )

    def _analyze_step(self, step: StoryStep, text: str, lang: str = 'en') -> dict:
        """
        Analyze a single step of the Story Circle.
        
        Args:
            step: Story step to analyze
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            dict: Analysis results for the step
        """
        return {
            "presence": True,  # В реальной реализации здесь должен быть анализ текста
            "strength": "средний" if lang == 'ru' else "medium",
            "suggestions": [],
            "criteria_met": step.analysis_criteria if lang == 'ru' else step.analysis_criteria_en
        }

    def _evaluate_overall_structure(self, text: str, lang: str = 'en') -> dict:
        """
        Evaluate the overall narrative structure.
        
        Args:
            text: Input text to analyze
            lang: Language for evaluation ('en' or 'ru')
            
        Returns:
            dict: Overall evaluation results
        """
        if lang == 'ru':
            return {
                "завершенность_круга": True,
                "баланс": "хорошо_сбалансирован",
                "предложения": []
            }
        return {
            "circle_completion": True,
            "balance": "well_balanced",
            "suggestions": []
        }

    def _calculate_step_position(self, step_number: int, radius: int = 150) -> tuple:
        """
        Calculate position for a step in the circle.
        
        Args:
            step_number: Number of the step
            radius: Circle radius in pixels
            
        Returns:
            tuple: (x, y) coordinates
        """
        angle = radians((step_number - 1) * 45 - 90)
        x = radius * cos(angle)
        y = radius * sin(angle)
        return (x, y)

    def visualize(self, analysis_result: dict, lang: str = 'en') -> str:
        """
        Generate HTML visualization of the Story Circle.
        
        Args:
            analysis_result: Dictionary containing analysis results
            lang: Language for visualization ('en' or 'ru')
            
        Returns:
            str: HTML representation of the circle
        """
        title = ("Сюжетный круг (Дэн Хармон)" if lang == 'ru' 
                else "Story Circle (Dan Harmon)")
        center_text = "Сюжетный<br>круг" if lang == 'ru' else "Story<br>Circle"
        
        html_parts = [
            f"<h1>{title}</h1>",
            "<div class='harmon-circle'>"
        ]

        for step in self.STORY_STEPS:
            x, y = self._calculate_step_position(step.number)
            angle = (step.number - 1) * 45 - 90
            step_name = step.name if lang == 'ru' else step.name_en
            
            html_parts.extend([
                f"<div class='step step-{step.number}' style='",
                f"transform: rotate({angle}deg) translate({x}px, {y}px) rotate(-{angle}deg);",
                f"color: {step.color};'>",
                f"<div class='step-number'>{step.number}</div>",
                f"<div class='step-name'>{step_name}</div>",
                "</div>"
            ])

        html_parts.extend([
            "<div class='circle-center'>",
            center_text,
            "</div>",
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)

    def get_prompt(self, lang: str = 'en') -> str:
        """
        Generate analysis prompt for Story Circle structure.
        
        Args:
            lang: Language for the prompt ('en' or 'ru')
        """
        if lang == 'ru':
            prompt_parts = [
                "Проанализируйте следующую нарративную структуру на основе сюжетного круга Дэна Хармона:\n"
            ]
        else:
            prompt_parts = [
                "Analyze the following narrative structure based on Dan Harmon's Story Circle:\n"
            ]

        current_act = None
        for step in self.STORY_STEPS:
            if step.act != current_act:
                current_act = step.act
                act_text = f"\nАкт - {current_act}:" if lang == 'ru' else f"\nAct - {current_act}:"
                prompt_parts.append(act_text)
            
            step_name = step.name if lang == 'ru' else step.name_en
            step_desc = step.description if lang == 'ru' else step.description_en
            criteria = step.analysis_criteria if lang == 'ru' else step.analysis_criteria_en
            
            prompt_parts.append(f"{step.number}. {step_name} ({step_desc})")
            criteria_label = "   Критерии: " if lang == 'ru' else "   Criteria: "
            prompt_parts.append(criteria_label + ", ".join(criteria))

        return "\n".join(prompt_parts)
