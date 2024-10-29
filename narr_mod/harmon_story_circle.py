# narr_mod/harmon_story_circle.py

from dataclasses import dataclass
from typing import List, Dict, Final, ClassVar
from math import cos, sin, radians
from narr_mod import NarrativeStructure

@dataclass
class StoryStep:
    number: int
    name: str
    description: str
    color: str
    act: str
    analysis_criteria: List[str]

class HarmonStoryCircle(NarrativeStructure):
    """Implementation of Dan Harmon's Story Circle narrative structure."""

    # Константы для актов
    ACT_BEGINNING: Final[str] = "Beginning"
    ACT_MIDDLE: Final[str] = "Middle"
    ACT_END: Final[str] = "End"

    # Определение шагов
    STORY_STEPS: ClassVar[List[StoryStep]] = [
        StoryStep(
            1, "Зона комфорта", 
            "Comfort Zone",
            "#e74c3c",
            ACT_BEGINNING,
            ["character establishment", "initial world state", "status quo"]
        ),
        StoryStep(
            2, "Потребность или желание",
            "Need or Desire",
            "#3498db",
            ACT_BEGINNING,
            ["motivation clarity", "stakes establishment", "goal definition"]
        ),
        StoryStep(
            3, "Незнакомая ситуация",
            "Unfamiliar Situation",
            "#2ecc71",
            ACT_MIDDLE,
            ["comfort zone departure", "new challenges", "initial adaptation"]
        ),
        StoryStep(
            4, "Поиск и адаптация",
            "Search and Adaptation",
            "#f39c12",
            ACT_MIDDLE,
            ["challenge handling", "skill development", "world exploration"]
        ),
        StoryStep(
            5, "Получение желаемого",
            "Getting What They Wanted",
            "#9b59b6",
            ACT_MIDDLE,
            ["goal achievement", "price recognition", "consequence understanding"]
        ),
        StoryStep(
            6, "Плата за него",
            "Paying the Price",
            "#e67e22",
            ACT_MIDDLE,
            ["sacrifice measurement", "cost evaluation", "change catalyst"]
        ),
        StoryStep(
            7, "Возвращение к привычному",
            "Return to Familiar",
            "#1abc9c",
            ACT_END,
            ["integration of change", "world comparison", "growth recognition"]
        ),
        StoryStep(
            8, "Способность меняться",
            "Changed State",
            "#34495e",
            ACT_END,
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

    def name(self) -> str:
        return "Story Circle (Dan Harmon)"

    def analyze(self, formatted_structure: dict) -> dict:
        """
        Analyze the narrative structure according to Harmon's Story Circle.
        
        Args:
            formatted_structure: Dictionary containing the narrative structure
            
        Returns:
            dict: Analysis results with step evaluation
        """
        analysis = {
            "steps": {
                step.name: self._analyze_step(step, formatted_structure)
                for step in self.STORY_STEPS
            },
            "overall_evaluation": self._evaluate_overall_structure(formatted_structure)
        }
        
        return {**formatted_structure, "analysis": analysis}

    def _analyze_step(self, step: StoryStep, structure: dict) -> dict:
        """Analyze a single step of the Story Circle."""
        return {
            "presence": True,  # Placeholder for actual analysis
            "strength": "medium",
            "suggestions": [],
            "criteria_met": step.analysis_criteria
        }

    def _evaluate_overall_structure(self, structure: dict) -> dict:
        """Evaluate the overall narrative structure."""
        return {
            "circle_completion": True,
            "balance": "well_balanced",
            "suggestions": []
        }

    def _calculate_step_position(self, step_number: int, radius: int = 150) -> tuple:
        """Calculate position for a step in the circle."""
        angle = radians((step_number - 1) * 45 - 90)
        x = radius * cos(angle)
        y = radius * sin(angle)
        return (x, y)

    def visualize(self, analysis_result: dict) -> str:
        """
        Generate HTML visualization of the Story Circle.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            str: HTML representation of the circle
        """
        html_parts = [
            "<h1>Сюжетный круг (Дэн Хармон)</h1>",
            "<div class='harmon-circle'>"
        ]

        # Добавляем шаги
        for step in self.STORY_STEPS:
            x, y = self._calculate_step_position(step.number)
            angle = (step.number - 1) * 45 - 90
            
            html_parts.extend([
                f"<div class='step step-{step.number}' style='",
                f"transform: rotate({angle}deg) translate({x}px, {y}px) rotate(-{angle}deg);",
                f"color: {step.color};'>",
                f"<div class='step-number'>{step.number}</div>",
                f"<div class='step-name'>{step.name}</div>",
                "</div>"
            ])

        # Добавляем центр круга
        html_parts.extend([
            "<div class='circle-center'>",
            "Story<br>Circle",
            "</div>",
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)

    def get_prompt(self) -> str:
        """Generate analysis prompt for Story Circle structure."""
        prompt_parts = [
            "Analyze the following narrative structure based on Dan Harmon's Story Circle:\n"
        ]

        current_act = None
        for step in self.STORY_STEPS:
            if step.act != current_act:
                current_act = step.act
                prompt_parts.append(f"\nAct - {current_act}:")
            
            prompt_parts.append(f"{step.number}. {step.name} ({step.description})")
            prompt_parts.append("   Criteria: " + ", ".join(step.analysis_criteria))

        return "\n".join(prompt_parts)
