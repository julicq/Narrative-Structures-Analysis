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
    name_en: str
    description: str
    description_en: str
    importance: int  # 1-10
    check_keywords: List[str]
    check_keywords_en: List[str]

@dataclass
class Act:
    number: int
    type: ActType
    name: str
    name_en: str
    description: str
    description_en: str
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

    @property
    def structure_type(self) -> StructureType:
        return StructureType.THREE_ACT

    MIN_ACT_LENGTH: Final[int] = 1000
    IDEAL_PROPORTIONS: Final[Dict[ActType, float]] = {
        ActType.SETUP: 0.25,
        ActType.CONFRONTATION: 0.5,
        ActType.RESOLUTION: 0.25
    }

    ACTS: ClassVar[List[Act]] = [
        Act(
            1,
            ActType.SETUP,
            "Завязка", "Setup",
            "Установка мира и персонажей",
            "Establishment of the world and characters",
            "#e6f3ff",
            [
                ActElement(
                    "Место действия", "Setting",
                    "Установка мира", "World establishment",
                    8,
                    ["мир", "место", "окружение", "среда"],
                    ["world", "setting", "place", "environment"]
                ),
                ActElement(
                    "Персонажи", "Characters",
                    "Представление главного героя",
                    "Main character introduction",
                    9,
                    ["протагонист", "герой", "персонаж", "главный"],
                    ["protagonist", "character", "hero", "main"]
                ),
                ActElement(
                    "Начальный конфликт", "Initial Conflict",
                    "Введение проблемы или вызова",
                    "Problem or challenge introduction",
                    7,
                    ["проблема", "конфликт", "вызов", "задача"],
                    ["problem", "conflict", "challenge", "issue"]
                )
            ],
            0.25
        ),
        Act(
            2,
            ActType.CONFRONTATION,
            "Конфронтация", "Confrontation",
            "Развитие конфликта и повышение ставок",
            "Development of conflict and raising stakes",
            "#fff2e6",
            [
                ActElement(
                    "Развитие конфликта", "Conflict Development",
                    "Эскалация основного конфликта",
                    "Escalation of the main conflict",
                    9,
                    ["эскалация", "развитие", "рост", "усиление"],
                    ["escalate", "develop", "grow", "increase"]
                ),
                ActElement(
                    "Ставки", "Stakes",
                    "Что поставлено на карту",
                    "What's at risk",
                    8,
                    ["ставки", "риск", "цена", "последствия"],
                    ["stakes", "risk", "cost", "consequence"]
                ),
                ActElement(
                    "Осложнения", "Complications",
                    "Дополнительные вызовы",
                    "Additional challenges",
                    7,
                    ["препятствие", "осложнение", "трудность", "проблема"],
                    ["obstacle", "complication", "difficulty", "problem"]
                )
            ],
            0.5
        ),
        Act(
            3,
            ActType.RESOLUTION,
            "Развязка", "Resolution",
            "Кульминация и разрешение конфликтов",
            "Climax and resolution of conflicts",
            "#e6ffe6",
            [
                ActElement(
                    "Кульминация", "Climax",
                    "Пик конфликта",
                    "Peak of the conflict",
                    9,
                    ["кульминация", "пик", "вершина", "высшая точка"],
                    ["climax", "peak", "culmination", "height"]
                ),
                ActElement(
                    "Разрешение", "Resolution",
                    "Как разрешаются конфликты",
                    "How conflicts are resolved",
                    8,
                    ["разрешение", "решение", "заключение", "конец"],
                    ["resolve", "solution", "conclusion", "end"]
                ),
                ActElement(
                    "Новый статус", "New Status",
                    "Достижение нового равновесия",
                    "New equilibrium achieved",
                    7,
                    ["изменение", "трансформация", "новый", "другой"],
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

    def analyze(self, text: str, lang: str = 'en') -> AnalysisResult:
        """
        Analyze the narrative structure according to the Three-Act Structure.
        
        Args:
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            AnalysisResult: Analysis results with detailed evaluation
        """
        acts_content = self._split_into_acts(text)
        
        act_analyses = {}
        for act in self.ACTS:
            act_content = acts_content.get(act.type, "")
            act_analyses[f"Act{act.number}"] = self._analyze_act(act, act_content, lang)

        structure = {
            "acts": act_analyses,
            "overall": self._analyze_overall_structure(acts_content, act_analyses, lang)
        }

        metadata = AnalysisMetadata(
            model_name="gpt-4",
            model_version="1.0",
            confidence=0.85,
            processing_time=1.0,
            structure_type=self.structure_type,
            display_name=self.display_name
        )

        summary = ("Анализ повествования с использованием трехактной структуры" 
                  if lang == 'ru' else 
                  "Analysis of narrative using Three-Act Structure")

        visualization = self.visualize(structure, lang)

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

    def _analyze_act(self, act: Act, content: str, lang: str = 'en') -> ActAnalysis:
        """Analyze a single act of the structure."""
        elements_present = {}
        strengths = []
        weaknesses = []
        suggestions = []
        
        for element in act.elements:
            keywords = element.check_keywords if lang == 'ru' else element.check_keywords_en
            element_name = element.name if lang == 'ru' else element.name_en
            
            is_present = any(keyword in content.lower() for keyword in keywords)
            elements_present[element_name] = is_present
            
            if is_present:
                strengths.append(
                    f"{element_name} хорошо установлен" if lang == 'ru' 
                    else f"{element_name} is well established"
                )
            else:
                weaknesses.append(
                    f"{element_name} требует доработки" if lang == 'ru'
                    else f"{element_name} needs more development"
                )
                suggestions.append(
                    f"Рассмотрите возможность добавления деталей о {element_name.lower()}" 
                    if lang == 'ru'
                    else f"Consider adding more details about {element_name.lower()}"
                )

        score = sum(elements_present.values()) / len(act.elements)

        return ActAnalysis(
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            score=score,
            elements_present=elements_present
        )

    def _analyze_overall_structure(
        self, 
        structure: dict, 
        act_analyses: Dict[str, ActAnalysis],
        lang: str = 'en'
    ) -> dict:
        """Analyze the overall structure balance and effectiveness."""
        return {
            "balance": self._analyze_balance(structure),
            "effectiveness": self._analyze_effectiveness(act_analyses),
            "suggestions": self._generate_overall_suggestions(act_analyses, lang)
        }
    
    def _analyze_effectiveness(self, act_analyses: Dict[str, ActAnalysis]) -> float:
        return sum(analysis.score for analysis in act_analyses.values()) / len(act_analyses)

    def _generate_overall_suggestions(
        self, 
        act_analyses: Dict[str, ActAnalysis],
        lang: str = 'en'
    ) -> List[str]:
        suggestions = []
        for act_name, analysis in act_analyses.items():
            if analysis.score < 0.7:
                suggestions.extend(analysis.suggestions)
        return suggestions

    def visualize(self, analysis_result: dict, lang: str = 'en') -> str:
        """
        Generate HTML visualization of the Three-Act Structure.
        
        Args:
            analysis_result: Dictionary containing analysis results
            lang: Language for visualization ('en' or 'ru')
            
        Returns:
            str: HTML representation of the structure
        """
        title = "Трехактная структура" if lang == 'ru' else "Three-Act Structure"
        html_parts = [
            f"<h2>{title}</h2>",
            "<div class='three-act-structure'>"
        ]

        for act in self.ACTS:
            act_analysis = analysis_result.get(f"Act{act.number}", {})
            act_name = act.name if lang == 'ru' else act.name_en
            
            html_parts.extend([
                f"<div class='act' style='background-color: {act.color}'>",
                f"<h3>{act_name}</h3>",
                "<div class='elements-list'>"
            ])

            for element in act.elements:
                element_name = element.name if lang == 'ru' else element.name_en
                is_present = act_analysis.get("elements_present", {}).get(element_name, False)
                status_class = "present" if is_present else "missing"
                
                html_parts.append(
                    f"<div class='element'>"
                    f"<span class='element-status {status_class}'></span>"
                    f"{element_name}"
                    f"</div>"
                )

            if act_analysis:
                score_text = "Оценка" if lang == 'ru' else "Score"
                html_parts.append(
                    "<div class='analysis-section'>"
                    f"<p>{score_text}: {act_analysis.get('score', 0):.2f}</p>"
                    "</div>"
                )

            html_parts.append("</div></div>")

        html_parts.extend([
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)

    def get_prompt(self, lang: str = 'en') -> str:
        """
        Generate analysis prompt for the Three-Act Structure.
        
        Args:
            lang: Language for the prompt ('en' or 'ru')
        """
        if lang == 'ru':
            prompt_parts = [
                "Проанализируйте следующую нарративную структуру на основе трехактной структуры:\n"
            ]
        else:
            prompt_parts = [
                "Analyze the following narrative structure based on the Three-Act Structure:\n"
            ]

        for act in self.ACTS:
            act_name = act.name if lang == 'ru' else act.name_en
            act_desc = act.description if lang == 'ru' else act.description_en
            
            prompt_parts.extend([
                f"\n{act_name} ({act_desc})",
                "Ключевые элементы для рассмотрения:" if lang == 'ru' else "Key elements to consider:"
            ])
            
            for element in act.elements:
                element_name = element.name if lang == 'ru' else element.name_en
                element_desc = element.description if lang == 'ru' else element.description_en
                importance_text = "Важность" if lang == 'ru' else "Importance"
                
                prompt_parts.append(
                    f"- {element_name}: {element_desc} "
                    f"({importance_text}: {element.importance}/10)"
                )

        return "\n".join(prompt_parts)

    def _analyze_balance(self, structure: dict) -> str:
        """Analyze the balance between acts."""
        total_length = sum(len(content) for content in structure.values())
        if total_length == 0:
            return "balanced" # или "сбалансировано" в зависимости от языка
            
        actual_proportions = {
            act_type: len(content) / total_length 
            for act_type, content in structure.items()
        }
        
        max_deviation = max(
            abs(actual - ideal)
            for (act_type, actual), (_, ideal) 
            in zip(actual_proportions.items(), self.IDEAL_PROPORTIONS.items())
        )
        
        if max_deviation <= 0.05:
            return "well_balanced"
        elif max_deviation <= 0.1:
            return "slightly_unbalanced"
        else:
            return "significantly_unbalanced"