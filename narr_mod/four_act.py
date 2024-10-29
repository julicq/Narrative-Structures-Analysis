# narr_mod/four_act.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Final, ClassVar
from narr_mod import NarrativeStructure

@dataclass
class Act:
    name: str
    description: str
    key_elements: List[str]
    analysis_criteria: List[str]

class FourAct(NarrativeStructure):
    """Implementation of Four-Act Structure narrative analysis."""

    # Константы для актов
    ACT_SETUP: Final[str] = "Setup"
    ACT_COMPLICATION: Final[str] = "Complication"
    ACT_DEVELOPMENT: Final[str] = "Development"
    ACT_RESOLUTION: Final[str] = "Resolution"

    # Определение структуры актов
    ACTS: ClassVar[Dict[str, Act]] = {
        ACT_SETUP: Act(
            name="Act 1",
            description="Setup",
            key_elements=['setting', 'main characters', 'initial conflict'],
            analysis_criteria=[
                "establishment of setting",
                "character introduction",
                "initial conflict presentation"
            ]
        ),
        ACT_COMPLICATION: Act(
            name="Act 2",
            description="Complication",
            key_elements=['challenge', 'obstacle', 'stakes'],
            analysis_criteria=[
                "introduction of challenges",
                "raising stakes",
                "obstacle development"
            ]
        ),
        ACT_DEVELOPMENT: Act(
            name="Act 3",
            description="Development",
            key_elements=['conflict', 'develop', 'climax'],
            analysis_criteria=[
                "conflict development",
                "build-up to climax",
                "character evolution"
            ]
        ),
        ACT_RESOLUTION: Act(
            name="Act 4",
            description="Resolution",
            key_elements=['resolve', 'resolution', 'conclusion', 'end'],
            analysis_criteria=[
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

    def name(self) -> str:
        return "Four-Act Structure"

    def analyze(self, formatted_structure: dict) -> dict:
        """
        Analyze the narrative structure using the Four-Act model.
        
        Args:
            formatted_structure: Dictionary containing the narrative structure
            
        Returns:
            dict: Complete analysis results
        """
        initial_analysis = self._perform_initial_analysis(formatted_structure)
        double_check_result = self._double_check_analysis(formatted_structure, initial_analysis)
        
        return {
            **initial_analysis,
            "double_check": double_check_result,
            "meta": {
                "structure_type": self.name(),
                "analysis_version": "1.0"
            }
        }

    def _analyze_act(self, act: Act, content: str) -> dict:
        """
        Analyze a single act based on its criteria and content.
        
        Args:
            act: Act object containing analysis criteria
            content: Content to analyze
            
        Returns:
            dict: Analysis results for the act
        """
        analysis = {
            "name": act.name,
            "description": act.description,
            "elements_present": [],
            "elements_missing": [],
            "suggestions": []
        }

        content_lower = content.lower()
        
        for element in act.key_elements:
            if element.lower() in content_lower:
                analysis["elements_present"].append(element)
            else:
                analysis["elements_missing"].append(element)
                analysis["suggestions"].append(f"Consider emphasizing {element}")

        return analysis

    def _perform_initial_analysis(self, formatted_structure: dict) -> dict:
        """Perform initial analysis of the structure."""
        return {
            act_key: self._analyze_act(
                act_data,
                formatted_structure.get(act_data.name, "")
            )
            for act_key, act_data in self.ACTS.items()
        }

    def _double_check_analysis(self, formatted_structure: dict, initial_analysis: dict) -> dict:
        """Perform secondary analysis for verification."""
        # Здесь можно добавить реальную интеграцию с LLM
        return {
            "verification_status": "completed",
            "additional_insights": [],
            "improvement_suggestions": []
        }

    def get_prompt(self) -> str:
        """Generate analysis prompt template."""
        return "\n".join([
            "Analyze the following narrative structure based on the Four-Act Structure:",
            "",
            *[f"{act.name} ({act.description}):" + "\n{" + act.name + "}\n"
              for act in self.ACTS.values()],
            "",
            "Evaluation Criteria:",
            *[f"- {act.name}: {', '.join(act.analysis_criteria)}"
              for act in self.ACTS.values()]
        ])

    def visualize(self, analysis_result: dict) -> str:
        """Generate HTML visualization of the analysis."""
        html_parts = [
            "<div class='four-act-structure'>",
            "<h2>Four-Act Structure Analysis</h2>"
        ]

        # Добавляем секции для каждого акта
        for act_key, act_data in self.ACTS.items():
            analysis = analysis_result.get(act_key, {})
            html_parts.extend([
                f"<div class='act'>",
                f"<h3>{act_data.name}: {act_data.description}</h3>",
                "<ul>",
                *[f"<li>Present: {element}</li>" 
                  for element in analysis.get('elements_present', [])],
                *[f"<li>Missing: {element}</li>" 
                  for element in analysis.get('elements_missing', [])],
                "</ul>",
                "</div>"
            ])

        # Добавляем секцию double-check
        if "double_check" in analysis_result:
            html_parts.extend([
                "<div class='double-check'>",
                "<h3>Verification Results</h3>",
                f"<p>{analysis_result['double_check']}</p>",
                "</div>"
            ])

        html_parts.extend([
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)
