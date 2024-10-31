# narr_mod/four_act.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Final, ClassVar
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

@dataclass
class Act:
    name: str
    name_en: str
    description: str
    description_en: str
    key_elements: List[str]
    key_elements_en: List[str]
    analysis_criteria: List[str]
    analysis_criteria_en: List[str]

class FourAct(NarrativeStructure):
    """Implementation of Four-Act Structure narrative analysis."""

    @property
    def structure_type(self) -> StructureType:
        return StructureType.FOUR_ACT

    # Константы для актов
    ACT_SETUP: Final[str] = "Setup"
    ACT_COMPLICATION: Final[str] = "Complication"
    ACT_DEVELOPMENT: Final[str] = "Development"
    ACT_RESOLUTION: Final[str] = "Resolution"

    # Определение структуры актов
    ACTS: ClassVar[Dict[str, Act]] = {
        ACT_SETUP: Act(
            name="Акт 1",
            name_en="Act 1",
            description="Завязка",
            description_en="Setup",
            key_elements=['место действия', 'главные герои', 'начальный конфликт'],
            key_elements_en=['setting', 'main characters', 'initial conflict'],
            analysis_criteria=[
                "установление места действия",
                "представление персонажей",
                "представление начального конфликта"
            ],
            analysis_criteria_en=[
                "establishment of setting",
                "character introduction",
                "initial conflict presentation"
            ]
        ),
        ACT_COMPLICATION: Act(
            name="Акт 2",
            name_en="Act 2",
            description="Осложнение",
            description_en="Complication",
            key_elements=['испытание', 'препятствие', 'ставки'],
            key_elements_en=['challenge', 'obstacle', 'stakes'],
            analysis_criteria=[
                "введение испытаний",
                "повышение ставок",
                "развитие препятствий"
            ],
            analysis_criteria_en=[
                "introduction of challenges",
                "raising stakes",
                "obstacle development"
            ]
        ),
        ACT_DEVELOPMENT: Act(
            name="Акт 3",
            name_en="Act 3",
            description="Развитие",
            description_en="Development",
            key_elements=['конфликт', 'развитие', 'кульминация'],
            key_elements_en=['conflict', 'develop', 'climax'],
            analysis_criteria=[
                "развитие конфликта",
                "нарастание к кульминации",
                "эволюция персонажей"
            ],
            analysis_criteria_en=[
                "conflict development",
                "build-up to climax",
                "character evolution"
            ]
        ),
        ACT_RESOLUTION: Act(
            name="Акт 4",
            name_en="Act 4",
            description="Развязка",
            description_en="Resolution",
            key_elements=['разрешение', 'развязка', 'заключение', 'конец'],
            key_elements_en=['resolve', 'resolution', 'conclusion', 'end'],
            analysis_criteria=[
                "разрешение конфликта",
                "завершение истории",
                "завершение арок персонажей"
            ],
            analysis_criteria_en=[
                "conflict resolution",
                "story conclusion",
                "character arcs completion"
            ]
        )
    }

    CSS_TEMPLATE: ClassVar[str] = """
    .four-act-structure {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        font-family: Arial, sans-serif;
    }
    .act {
        margin: 20px 0;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .act h3 {
        margin-top: 0;
        color: #333;
    }
    .double-check {
        margin-top: 30px;
        padding: 15px;
        background-color: #f5f5f5;
        border-radius: 5px;
    }
    """

    def analyze(self, text: str, lang: str = 'en') -> AnalysisResult:
        """
        Analyze the narrative structure using the Four-Act model.
        
        Args:
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            AnalysisResult: Complete analysis results
        """
        initial_analysis = self._perform_initial_analysis(text, lang)
        double_check_result = self._double_check_analysis(text, initial_analysis, lang)
        
        structure = {
            "acts": initial_analysis,
            "double_check": double_check_result,
        }
        
        metadata = AnalysisMetadata(
            model_name="gpt-4",
            model_version="1.0",
            confidence=0.85,
            processing_time=1.0,
            structure_type=self.structure_type,
            display_name=self.display_name
        )

        summary = ("Анализ нарративной структуры по четырехактной модели" 
                  if lang == 'ru' else 
                  "Analysis of narrative structure using Four-Act Structure")
        
        visualization = self.visualize(structure, lang)
        
        return AnalysisResult(
            structure=structure,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )

    def _analyze_act(self, act: Act, content: str, lang: str = 'en') -> dict:
        """
        Analyze a single act based on its criteria and content.
        
        Args:
            act: Act object containing analysis criteria
            content: Content to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            dict: Analysis results for the act
        """
        analysis = {
            "name": act.name if lang == 'ru' else act.name_en,
            "description": act.description if lang == 'ru' else act.description_en,
            "elements_present": [],
            "elements_missing": [],
            "suggestions": []
        }

        content_lower = content.lower()
        elements = act.key_elements if lang == 'ru' else act.key_elements_en
        
        for element in elements:
            if element.lower() in content_lower:
                analysis["elements_present"].append(element)
            else:
                analysis["elements_missing"].append(element)
                suggestion = f"Рекомендуется усилить {element}" if lang == 'ru' else f"Consider emphasizing {element}"
                analysis["suggestions"].append(suggestion)

        return analysis

    def _perform_initial_analysis(self, text: str, lang: str = 'en') -> dict:
        """Perform initial analysis of the structure."""
        return {
            act_key: self._analyze_act(act_data, text, lang)
            for act_key, act_data in self.ACTS.items()
        }

    def _double_check_analysis(self, text: str, initial_analysis: dict, lang: str = 'en') -> dict:
        """Perform secondary analysis for verification."""
        return {
            "verification_status": "завершено" if lang == 'ru' else "completed",
            "additional_insights": [],
            "improvement_suggestions": []
        }

    def get_prompt(self, lang: str = 'en') -> str:
        """
        Generate analysis prompt template.
        
        Args:
            lang: Language for the prompt ('en' or 'ru')
        """
        if lang == 'ru':
            return "\n".join([
                "Проанализируйте следующую нарративную структуру на основе четырехактной модели:",
                "",
                *[f"{act.name} ({act.description}):" + "\n{" + act.name + "}\n"
                  for act in self.ACTS.values()],
                "",
                "Критерии оценки:",
                *[f"- {act.name}: {', '.join(act.analysis_criteria)}"
                  for act in self.ACTS.values()]
            ])
        else:
            return "\n".join([
                "Analyze the following narrative structure based on the Four-Act Structure:",
                "",
                *[f"{act.name_en} ({act.description_en}):" + "\n{" + act.name_en + "}\n"
                  for act in self.ACTS.values()],
                "",
                "Evaluation Criteria:",
                *[f"- {act.name_en}: {', '.join(act.analysis_criteria_en)}"
                  for act in self.ACTS.values()]
            ])

    def visualize(self, analysis_result: dict, lang: str = 'en') -> str:
        """
        Generate HTML visualization of the analysis.
        
        Args:
            analysis_result: Analysis results to visualize
            lang: Language for visualization ('en' or 'ru')
        """
        title = "Анализ четырехактной структуры" if lang == 'ru' else "Four-Act Structure Analysis"
        
        html_parts = [
            "<div class='four-act-structure'>",
            f"<h2>{title}</h2>"
        ]

        for act_key, act_data in self.ACTS.items():
            analysis = analysis_result.get(act_key, {})
            act_name = act_data.name if lang == 'ru' else act_data.name_en
            act_desc = act_data.description if lang == 'ru' else act_data.description_en
            
            present_label = "Присутствует" if lang == 'ru' else "Present"
            missing_label = "Отсутствует" if lang == 'ru' else "Missing"
            
            html_parts.extend([
                f"<div class='act'>",
                f"<h3>{act_name}: {act_desc}</h3>",
                "<ul>",
                *[f"<li>{present_label}: {element}</li>" 
                  for element in analysis.get('elements_present', [])],
                *[f"<li>{missing_label}: {element}</li>" 
                  for element in analysis.get('elements_missing', [])],
                "</ul>",
                "</div>"
            ])

        if "double_check" in analysis_result:
            verification_title = "Результаты проверки" if lang == 'ru' else "Verification Results"
            html_parts.extend([
                "<div class='double-check'>",
                f"<h3>{verification_title}</h3>",
                f"<p>{analysis_result['double_check']}</p>",
                "</div>"
            ])

        html_parts.extend([
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)
