# narr_mod/three_act.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Final, ClassVar
from enum import Enum
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

class ActType(Enum):
    SETUP = "Setup"
    CONFRONTATION = "Confrontation"
    RESOLUTION = "Resolution"

@dataclass
class ActElement:
    name: str
    description: str
    importance: int  # 1-10
    check_keywords: List[str]

@dataclass
class Act:
    number: int
    type: ActType
    name: str
    description: str
    color: str
    elements: List[ActElement]
    expected_length: float  # процент от общей длины

@dataclass
class AnalysisResult:
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    score: float  # 0-1
    elements_present: Dict[str, bool]

@dataclass
class ActAnalysis:
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    score: float  # 0-1
    elements_present: Dict[str, bool]

class ThreeAct(NarrativeStructure):
    """Implementation of the Three-Act Structure narrative analysis."""

    # Добавляем реализацию абстрактного метода structure_type
    @property
    def structure_type(self) -> StructureType:
        return StructureType.THREE_ACT

    # Константы
    MIN_ACT_LENGTH: Final[int] = 1000  # минимальная длина акта в символах
    IDEAL_PROPORTIONS: Final[Dict[ActType, float]] = {
        ActType.SETUP: 0.25,
        ActType.CONFRONTATION: 0.5,
        ActType.RESOLUTION: 0.25
    }

    # Определение структуры актов
    ACTS: ClassVar[List[Act]] = [
        Act(
            1,
            ActType.SETUP,
            "Setup",
            "Establishment of the world and characters",
            "#e6f3ff",
            [
                ActElement(
                    "Setting",
                    "World establishment",
                    8,
                    ["world", "setting", "place", "environment"]
                ),
                ActElement(
                    "Characters",
                    "Main character introduction",
                    9,
                    ["protagonist", "character", "hero", "main"]
                ),
                ActElement(
                    "Initial Conflict",
                    "Problem or challenge introduction",
                    7,
                    ["problem", "conflict", "challenge", "issue"]
                )
            ],
            0.25
        ),
        Act(
            2,
            ActType.CONFRONTATION,
            "Confrontation",
            "Development of conflict and raising stakes",
            "#fff2e6",
            [
                ActElement(
                    "Conflict Development",
                    "Escalation of the main conflict",
                    9,
                    ["escalate", "develop", "grow", "increase"]
                ),
                ActElement(
                    "Stakes",
                    "What's at risk",
                    8,
                    ["stakes", "risk", "cost", "consequence"]
                ),
                ActElement(
                    "Complications",
                    "Additional challenges",
                    7,
                    ["obstacle", "complication", "difficulty", "problem"]
                )
            ],
            0.5
        ),
        Act(
            3,
            ActType.RESOLUTION,
            "Resolution",
            "Climax and resolution of conflicts",
            "#e6ffe6",
            [
                ActElement(
                    "Climax",
                    "Peak of the conflict",
                    9,
                    ["climax", "peak", "culmination", "height"]
                ),
                ActElement(
                    "Resolution",
                    "How conflicts are resolved",
                    8,
                    ["resolve", "solution", "conclusion", "end"]
                ),
                ActElement(
                    "New Status",
                    "New equilibrium achieved",
                    7,
                    ["change", "transformation", "new", "different"]
                )
            ],
            0.25
        )
    ]

    CSS_TEMPLATE: ClassVar[str] = """
        .three-act-structure {
            display: flex;
            justify-content: space-between;
            margin: 20px auto;
            max-width: 1200px;
            gap: 20px;
        }
        .act {
            flex: 1;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .act:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .act h3 {
            margin: 0 0 15px;
            font-size: 1.2em;
            color: #333;
        }
        .elements-list {
            list-style: none;
            padding: 0;
        }
        .element {
            margin: 10px 0;
            padding: 8px;
            background: rgba(255,255,255,0.7);
            border-radius: 4px;
        }
        .element-status {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .element-status.present {
            background-color: #2ecc71;
        }
        .element-status.missing {
            background-color: #e74c3c;
        }
        .analysis-section {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255,255,255,0.9);
            border-radius: 6px;
        }
    """

    def analyze(self, text: str) -> AnalysisResult:
        """
        Analyze the narrative structure according to the Three-Act Structure.
        
        Args:
            text: Input text to analyze
            
        Returns:
            AnalysisResult: Analysis results with detailed evaluation
        """
        # Разбиваем текст на акты (упрощенная версия)
        acts_content = self._split_into_acts(text)
        
        # Анализируем каждый акт
        act_analyses = {}
        for act in self.ACTS:
            act_content = acts_content.get(act.type, "")
            act_analyses[f"Act{act.number}"] = self._analyze_act(act, act_content)

        # Формируем структуру результата
        structure = {
            "acts": act_analyses,
            "overall": self._analyze_overall_structure(acts_content, act_analyses)
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

        # Создаем краткое описание
        summary = "Analysis of narrative using Three-Act Structure"

        # Создаем визуализацию
        visualization = self.visualize(structure)

        return AnalysisResult(
            structure=structure,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )
    
    def _split_into_acts(self, text: str) -> Dict[ActType, str]:
        """Split the text into three acts based on simple heuristics."""
        total_length = len(text)
        return {
            ActType.SETUP: text[:int(total_length * 0.25)],
            ActType.CONFRONTATION: text[int(total_length * 0.25):int(total_length * 0.75)],
            ActType.RESOLUTION: text[int(total_length * 0.75):]
        }

    def _analyze_act(self, act: Act, content: str) -> ActAnalysis:
        """Analyze a single act of the structure."""
        elements_present = {}
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Проверяем наличие каждого элемента
        for element in act.elements:
            is_present = any(keyword in content.lower() for keyword in element.check_keywords)
            elements_present[element.name] = is_present
            
            if is_present:
                strengths.append(f"{element.name} is well established")
            else:
                weaknesses.append(f"{element.name} needs more development")
                suggestions.append(f"Consider adding more details about {element.name.lower()}")

        # Рассчитываем общий счет
        score = sum(elements_present.values()) / len(act.elements)

        return ActAnalysis(
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            score=score,
            elements_present=elements_present
        )


    def _analyze_overall_structure(self, structure: dict, act_analyses: Dict[str, ActAnalysis]) -> dict:
        """Analyze the overall structure balance and effectiveness."""
        return {
            "balance": self._analyze_balance(structure),
            "effectiveness": self._analyze_effectiveness(act_analyses),
            "suggestions": self._generate_overall_suggestions(act_analyses)
        }
    
    def _analyze_effectiveness(self, act_analyses: Dict[str, ActAnalysis]) -> float:
        return sum(analysis.score for analysis in act_analyses.values()) / len(act_analyses)

    def _generate_overall_suggestions(self, act_analyses: Dict[str, ActAnalysis]) -> List[str]:
        suggestions = []
        for act_name, analysis in act_analyses.items():
            if analysis.score < 0.7:
                suggestions.extend(analysis.suggestions)
        return suggestions

    def visualize(self, analysis_result: dict) -> str:
        """
        Generate HTML visualization of the Three-Act Structure.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            str: HTML representation of the structure
        """
        html_parts = [
            "<h2>Трехактная структура</h2>",
            "<div class='three-act-structure'>"
        ]

        # Добавляем каждый акт
        for act in self.ACTS:
            act_analysis = analysis_result.get(f"Act{act.number}", {})
            
            html_parts.extend([
                f"<div class='act' style='background-color: {act.color}'>",
                f"<h3>Act {act.number}: {act.name}</h3>",
                "<div class='elements-list'>"
            ])

            # Добавляем элементы акта
            for element in act.elements:
                is_present = act_analysis.get("elements_present", {}).get(element.name, False)
                status_class = "present" if is_present else "missing"
                
                html_parts.append(
                    f"<div class='element'>"
                    f"<span class='element-status {status_class}'></span>"
                    f"{element.name}"
                    f"</div>"
                )

            # Добавляем анализ
            if act_analysis:
                html_parts.append(
                    "<div class='analysis-section'>"
                    f"<p>Score: {act_analysis.get('score', 0):.2f}</p>"
                    "</div>"
                )

            html_parts.append("</div></div>")

        html_parts.extend([
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)

    def get_prompt(self) -> str:
        """Generate analysis prompt for the Three-Act Structure."""
        prompt_parts = [
            "Analyze the following narrative structure based on the Three-Act Structure:\n"
        ]

        for act in self.ACTS:
            prompt_parts.extend([
                f"\nAct {act.number}: {act.name} ({act.description})",
                "Key elements to consider:"
            ])
            
            for element in act.elements:
                prompt_parts.append(
                    f"- {element.name}: {element.description} "
                    f"(Importance: {element.importance}/10)"
                )

        return "\n".join(prompt_parts)
