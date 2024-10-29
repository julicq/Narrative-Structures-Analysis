# narr_mod/watts_eight_point_arc.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Final, ClassVar
from enum import Enum
from narr_mod import NarrativeStructure

class ArcPhase(Enum):
    BEGINNING = "Beginning"
    MIDDLE = "Middle"
    END = "End"

@dataclass
class ArcPoint:
    number: int
    name: str
    phase: ArcPhase
    description: str
    keywords: List[str]
    importance: int  # 1-10
    color: str
    expected_length: float  # процент от общей длины

@dataclass
class AnalysisResult:
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    score: float  # 0-1
    keywords_found: Dict[str, bool]

class WattsEightPointArc(NarrativeStructure):
    """Implementation of Nigel Watts' Eight-Point Arc structure."""

    # Константы
    MIN_POINT_LENGTH: Final[int] = 500  # минимальная длина точки в символах
    TOTAL_POINTS: Final[int] = 8

    # Определение структуры арки
    POINTS: ClassVar[List[ArcPoint]] = [
        ArcPoint(
            1,
            "Stasis",
            ArcPhase.BEGINNING,
            "Initial equilibrium before the story begins",
            ["normal", "everyday", "routine", "balance", "ordinary"],
            8,
            "#e6f3ff",
            0.1
        ),
        ArcPoint(
            2,
            "Trigger",
            ArcPhase.BEGINNING,
            "Event that disrupts the stasis",
            ["disruption", "change", "catalyst", "incident", "trigger"],
            9,
            "#ffebcc",
            0.1
        ),
        ArcPoint(
            3,
            "Quest",
            ArcPhase.MIDDLE,
            "Protagonist's journey begins",
            ["journey", "goal", "mission", "pursuit", "objective"],
            9,
            "#e6ffe6",
            0.15
        ),
        ArcPoint(
            4,
            "Surprise",
            ArcPhase.MIDDLE,
            "Unexpected developments",
            ["unexpected", "twist", "revelation", "shock", "discovery"],
            8,
            "#ffe6e6",
            0.15
        ),
        ArcPoint(
            5,
            "Critical Choice",
            ArcPhase.MIDDLE,
            "Key decision point",
            ["decision", "choice", "dilemma", "crossroads", "turning"],
            10,
            "#fff2cc",
            0.15
        ),
        ArcPoint(
            6,
            "Climax",
            ArcPhase.MIDDLE,
            "Height of conflict",
            ["climax", "confrontation", "peak", "crisis", "showdown"],
            10,
            "#ffcccc",
            0.15
        ),
        ArcPoint(
            7,
            "Reversal",
            ArcPhase.END,
            "Consequences of the climax",
            ["aftermath", "change", "consequence", "effect", "result"],
            8,
            "#e6f2ff",
            0.1
        ),
        ArcPoint(
            8,
            "Resolution",
            ArcPhase.END,
            "New equilibrium",
            ["resolution", "conclusion", "ending", "closure", "settlement"],
            9,
            "#f2e6ff",
            0.1
        )
    ]

    CSS_TEMPLATE: ClassVar[str] = """
        .watts-arc {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        .arc-timeline {
            position: relative;
            padding: 20px 0;
        }
        .arc-point {
            display: flex;
            margin: 20px 0;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .arc-point:hover {
            transform: translateX(10px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .point-number {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
            background: rgba(0,0,0,0.1);
        }
        .point-content {
            flex: 1;
        }
        .point-name {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .point-description {
            color: #666;
            font-size: 0.9em;
        }
        .point-stats {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(0,0,0,0.1);
        }
        .keywords-found {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }
        .keyword {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            background: rgba(0,0,0,0.05);
        }
        .keyword.found {
            background: #4CAF50;
            color: white;
        }
    """

    def name(self) -> str:
        return "Eight Point Arc (Nigel Watts)"

    def analyze(self, formatted_structure: dict) -> dict:
        """
        Analyze the narrative structure according to Watts' Eight-Point Arc.
        
        Args:
            formatted_structure: Dictionary containing the narrative structure
            
        Returns:
            dict: Analysis results with detailed evaluation
        """
        analysis = {
            "points": {},
            "phases": {
                phase.value: self._analyze_phase(phase, formatted_structure)
                for phase in ArcPhase
            },
            "overall": self._analyze_overall_structure(formatted_structure)
        }

        for point in self.POINTS:
            analysis["points"][point.name] = self._analyze_point(point, formatted_structure)

        return analysis

    def _analyze_point(self, point: ArcPoint, content: dict) -> AnalysisResult:
        """Analyze a single point of the arc."""
        point_content = content.get(point.name.lower().replace(" ", "_"), "")
        
        keywords_found = {
            keyword: keyword.lower() in point_content.lower()
            for keyword in point.keywords
        }
        
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Анализ наличия ключевых слов
        found_keywords = sum(keywords_found.values())
        if found_keywords >= len(point.keywords) * 0.7:
            strengths.append(f"Strong presence of {point.name} elements")
        else:
            weaknesses.append(f"Weak representation of {point.name}")
            suggestions.append(f"Consider strengthening {point.name} by incorporating more relevant elements")

        # Анализ длины содержания
        if len(point_content) < self.MIN_POINT_LENGTH:
            weaknesses.append(f"{point.name} seems underdeveloped")
            suggestions.append(f"Expand the {point.name} section")

        score = found_keywords / len(point.keywords)

        return AnalysisResult(
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            score=score,
            keywords_found=keywords_found
        )

    def _analyze_phase(self, phase: ArcPhase, content: dict) -> dict:
        """Analyze a complete phase of the arc."""
        phase_points = [p for p in self.POINTS if p.phase == phase]
        phase_content = " ".join(
            content.get(p.name.lower().replace(" ", "_"), "")
            for p in phase_points
        )
        
        return {
            "length": len(phase_content),
            "points_count": len(phase_points),
            "balance": len(phase_content) / sum(len(content.get(p.name.lower().replace(" ", "_"), ""))
                                              for p in self.POINTS)
        }

    def _analyze_overall_structure(self, content: dict) -> dict:
        """Analyze the overall structure balance and effectiveness."""
        total_length = sum(len(content.get(p.name.lower().replace(" ", "_"), ""))
                          for p in self.POINTS)
        
        return {
            "total_length": total_length,
            "balance_score": self._calculate_balance_score(content),
            "progression_score": self._calculate_progression_score(content)
        }

    def visualize(self, analysis_result: dict) -> str:
        """
        Generate HTML visualization of the Eight-Point Arc.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            str: HTML representation of the arc
        """
        html_parts = [
            "<div class='watts-arc'>",
            "<h2>Eight-Point Arc Analysis</h2>",
            "<div class='arc-timeline'>"
        ]

        for point in self.POINTS:
            point_analysis = analysis_result.get("points", {}).get(point.name, {})
            score = point_analysis.get("score", 0)
            
            html_parts.append(f"""
                <div class='arc-point' style='background-color: {point.color}'>
                    <div class='point-number'>{point.number}</div>
                    <div class='point-content'>
                        <div class='point-name'>{point.name}</div>
                        <div class='point-description'>{point.description}</div>
                        <div class='point-stats'>
                            <div class='score'>Score: {score:.2f}</div>
                            <div class='keywords-found'>
                                {self._generate_keywords_html(point_analysis.get("keywords_found", {}))}
                            </div>
                        </div>
                    </div>
                </div>
            """)

        html_parts.extend([
            "</div>",  # close arc-timeline
            "</div>",  # close watts-arc
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)

    def _generate_keywords_html(self, keywords_found: Dict[str, bool]) -> str:
        """Generate HTML for keywords display."""
        return "".join(
            f"<span class='keyword {('found' if found else '')}'>{keyword}</span>"
            for keyword, found in keywords_found.items()
        )

    def get_prompt(self) -> str:
        """Generate analysis prompt for the Eight-Point Arc."""
        prompt_parts = [
            "Analyze the following narrative structure based on Nigel Watts' Eight-Point Arc:\n"
        ]

        current_phase = None
        for point in self.POINTS:
            if point.phase != current_phase:
                current_phase = point.phase
                prompt_parts.append(f"\n{current_phase.value}:")
            
            prompt_parts.extend([
                f"\n{point.number}. {point.name}",
                f"   Description: {point.description}",
                f"   Importance: {point.importance}/10",
                "   Key elements to look for:",
                "   " + ", ".join(point.keywords)
            ])

        return "\n".join(prompt_parts)
