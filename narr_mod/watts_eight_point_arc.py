# narr_mod/watts_eight_point_arc.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Final, ClassVar
from enum import Enum
from narr_mod import NarrativeStructure, StructureType, AnalysisResult as BaseAnalysisResult, AnalysisMetadata

class ArcPhase(Enum):
    BEGINNING = "Beginning"
    MIDDLE = "Middle"
    END = "End"

@dataclass
class ArcPoint:
    number: int
    name: str
    name_ru: str
    phase: ArcPhase
    description: str
    description_ru: str
    keywords: List[str]
    keywords_ru: List[str]
    importance: int  # 1-10
    color: str
    expected_length: float  # процент от общей длины

@dataclass
class PointAnalysis:
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    score: float  # 0-1
    keywords_found: Dict[str, bool]

class WattsEightPointArc(NarrativeStructure):
    """Implementation of Nigel Watts' Eight-Point Arc structure."""

    @property
    def structure_type(self) -> StructureType:
        return StructureType.WATTS_EIGHT_POINT

    MIN_POINT_LENGTH: Final[int] = 500
    TOTAL_POINTS: Final[int] = 8

    PHASE_NAMES = {
        'ru': {
            ArcPhase.BEGINNING: "Начало",
            ArcPhase.MIDDLE: "Середина",
            ArcPhase.END: "Конец"
        },
        'en': {
            ArcPhase.BEGINNING: "Beginning",
            ArcPhase.MIDDLE: "Middle",
            ArcPhase.END: "End"
        }
    }

    POINTS: ClassVar[List[ArcPoint]] = [
        ArcPoint(
            1,
            "Stasis",
            "Статичность",
            ArcPhase.BEGINNING,
            "Initial equilibrium before the story begins",
            "Начальное равновесие перед началом истории",
            ["normal", "everyday", "routine", "balance", "ordinary"],
            ["обычный", "повседневный", "рутина", "равновесие", "обыденный"],
            8,
            "#e6f3ff",
            0.1
        ),
        ArcPoint(
            2,
            "Trigger",
            "Триггер",
            ArcPhase.BEGINNING,
            "Event that disrupts the stasis",
            "Событие, нарушающее равновесие",
            ["disruption", "change", "catalyst", "incident", "trigger"],
            ["нарушение", "изменение", "катализатор", "происшествие", "триггер"],
            9,
            "#ffebcc",
            0.1
        ),
        ArcPoint(
            3,
            "Quest",
            "Поиск",
            ArcPhase.MIDDLE,
            "Protagonist's journey begins",
            "Начало пути протагониста",
            ["journey", "goal", "mission", "pursuit", "objective"],
            ["путь", "цель", "миссия", "стремление", "задача"],
            9,
            "#e6ffe6",
            0.15
        ),
        ArcPoint(
            4,
            "Surprise",
            "Сюрприз",
            ArcPhase.MIDDLE,
            "Unexpected developments",
            "Неожиданные повороты",
            ["unexpected", "twist", "revelation", "shock", "discovery"],
            ["неожиданность", "поворот", "откровение", "шок", "открытие"],
            8,
            "#ffe6e6",
            0.15
        ),
        ArcPoint(
            5,
            "Critical Choice",
            "Критический выбор",
            ArcPhase.MIDDLE,
            "Key decision point",
            "Ключевой момент принятия решения",
            ["decision", "choice", "dilemma", "crossroads", "turning"],
            ["решение", "выбор", "дилемма", "перепутье", "поворот"],
            10,
            "#fff2cc",
            0.15
        ),
        ArcPoint(
            6,
            "Climax",
            "Кульминация",
            ArcPhase.MIDDLE,
            "Height of conflict",
            "Пик конфликта",
            ["climax", "confrontation", "peak", "crisis", "showdown"],
            ["кульминация", "противостояние", "пик", "кризис", "развязка"],
            10,
            "#ffcccc",
            0.15
        ),
        ArcPoint(
            7,
            "Reversal",
            "Реверс",
            ArcPhase.END,
            "Consequences of the climax",
            "Последствия кульминации",
            ["aftermath", "change", "consequence", "effect", "result"],
            ["последствия", "изменение", "результат", "эффект", "итог"],
            8,
            "#e6f2ff",
            0.1
        ),
        ArcPoint(
            8,
            "Resolution",
            "Разрешение",
            ArcPhase.END,
            "New equilibrium",
            "Новое равновесие",
            ["resolution", "conclusion", "ending", "closure", "settlement"],
            ["разрешение", "заключение", "конец", "завершение", "урегулирование"],
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

    def analyze(self, text: str, lang: str = 'en') -> BaseAnalysisResult:
        """
        Analyze the narrative structure according to Watts' Eight-Point Arc.
        
        Args:
            text: Input text to analyze
            lang: Language code ('en' or 'ru')
            
        Returns:
            BaseAnalysisResult: Analysis results with detailed evaluation
        """
        formatted_structure = self._split_into_points(text)
        
        analysis = {
            "points": {},
            "phases": {
                self.PHASE_NAMES[lang][phase]: self._analyze_phase(phase, formatted_structure)
                for phase in ArcPhase
            },
            "overall": self._analyze_overall_structure(formatted_structure)
        }

        for point in self.POINTS:
            point_name = point.name if lang == 'en' else point.name_ru
            analysis["points"][point_name] = self._analyze_point(point, formatted_structure, lang)

        metadata = AnalysisMetadata(
            model_name="gpt-4",
            model_version="1.0",
            confidence=0.85,
            processing_time=1.0,
            structure_type=self.structure_type,
            display_name=self.display_name
        )

        summary = ("Анализ повествования по восьмиточечной арке Уоттса" 
                if lang == 'ru' else 
                "Analysis of narrative using Watts' Eight-Point Arc")

        visualization = self.visualize(analysis, lang)

        return BaseAnalysisResult(
            structure=analysis,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )

    def _split_into_points(self, text: str) -> Dict[str, str]:
        """Split the text into points based on expected lengths."""
        points_content = {}
        
        if not text:
            return {point.name.lower().replace(" ", "_"): "" 
                    for point in self.POINTS}
        
        total_length = len(text)
        current_pos = 0
        
        for point in self.POINTS:
            point_key = point.name.lower().replace(" ", "_")
            point_length = max(1, int(total_length * point.expected_length))
            end_pos = min(current_pos + point_length, total_length)
            
            if current_pos >= total_length:
                points_content[point_key] = ""
            else:
                text_chunk = text[current_pos:end_pos]
                sentence_end = text_chunk.rfind('. ')
                paragraph_end = text_chunk.rfind('\n')
                
                if sentence_end > 0:
                    end_pos = current_pos + sentence_end + 1
                elif paragraph_end > 0:
                    end_pos = current_pos + paragraph_end + 1
                    
                points_content[point_key] = text[current_pos:end_pos].strip()
                current_pos = end_pos
                
        return points_content

    def _analyze_point(self, point: ArcPoint, content: dict, lang: str = 'en') -> PointAnalysis:
        """Analyze a single point of the arc."""
        point_content = content.get(point.name.lower().replace(" ", "_"), "")
        
        keywords = point.keywords if lang == 'en' else point.keywords_ru
        point_name = point.name if lang == 'en' else point.name_ru
        
        keywords_found = {
            keyword: keyword.lower() in point_content.lower()
            for keyword in keywords
        }
        
        strengths = []
        weaknesses = []
        suggestions = []
        
        found_keywords = sum(keywords_found.values())
        if found_keywords >= len(keywords) * 0.7:
            strengths.append(
                f"Сильное присутствие элементов {point_name}" if lang == 'ru'
                else f"Strong presence of {point_name} elements"
            )
        else:
            weaknesses.append(
                f"Слабое представление {point_name}" if lang == 'ru'
                else f"Weak representation of {point_name}"
            )
            suggestions.append(
                f"Рекомендуется усилить {point_name}, добавив больше релевантных элементов" if lang == 'ru'
                else f"Consider strengthening {point_name} by incorporating more relevant elements"
            )

        if len(point_content) < self.MIN_POINT_LENGTH:
            weaknesses.append(
                f"{point_name} недостаточно развит" if lang == 'ru'
                else f"{point_name} seems underdeveloped"
            )
            suggestions.append(
                f"Расширьте раздел {point_name}" if lang == 'ru'
                else f"Expand the {point_name} section"
            )

        score = found_keywords / len(keywords)

        return PointAnalysis(
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

    def _calculate_balance_score(self, content: dict) -> float:
        """Calculate the balance score for the overall structure."""
        total_length = sum(len(content.get(p.name.lower().replace(" ", "_"), ""))
                        for p in self.POINTS)
        
        if total_length == 0:
            return 0.0
            
        deviations = []
        for point in self.POINTS:
            point_content = content.get(point.name.lower().replace(" ", "_"), "")
            expected_length = total_length * point.expected_length
            actual_length = len(point_content)
            deviation = abs(actual_length - expected_length) / expected_length
            deviations.append(deviation)
            
        return 1.0 - (sum(deviations) / len(deviations))

    def _calculate_progression_score(self, content: dict) -> float:
            """Calculate how well the narrative progresses through the points."""
            scores = []
            for i in range(len(self.POINTS) - 1):
                current_point = self.POINTS[i]
                next_point = self.POINTS[i + 1]
                
                current_content = content.get(current_point.name.lower().replace(" ", "_"), "")
                next_content = content.get(next_point.name.lower().replace(" ", "_"), "")
                
                # Проверяем связность между точками
                transition_score = self._analyze_transition(current_content, next_content)
                scores.append(transition_score)
                
            return sum(scores) / len(scores) if scores else 0.0

    def _analyze_transition(self, current_content: str, next_content: str) -> float:
        """
        Analyze transition between two points.
        Returns a score between 0 and 1.
        """
        if not current_content or not next_content:
            return 0.0
        
        # Простой анализ связности на основе общих слов
        current_words = set(current_content.lower().split())
        next_words = set(next_content.lower().split())
        
        common_words = current_words.intersection(next_words)
        total_words = current_words.union(next_words)
        
        if not total_words:
            return 0.0
        
        return len(common_words) / len(total_words)

    def visualize(self, analysis_result: dict, lang: str = 'en') -> str:
        """Generate HTML visualization of the Eight-Point Arc."""
        title = "Анализ восьмиточечной арки" if lang == 'ru' else "Eight-Point Arc Analysis"
        
        html_parts = [
            "<div class='watts-arc'>",
            f"<h2>{title}</h2>",
            "<div class='arc-timeline'>"
        ]

        for point in self.POINTS:
            point_name = point.name if lang == 'en' else point.name_ru
            point_desc = point.description if lang == 'en' else point.description_ru
            point_analysis = analysis_result.get("points", {}).get(point_name, {})
            score = point_analysis.get("score", 0)
            
            score_text = "Оценка" if lang == 'ru' else "Score"
            
            html_parts.append(f"""
                <div class='arc-point' style='background-color: {point.color}'>
                    <div class='point-number'>{point.number}</div>
                    <div class='point-content'>
                        <div class='point-name'>{point_name}</div>
                        <div class='point-description'>{point_desc}</div>
                        <div class='point-stats'>
                            <div class='score'>{score_text}: {score:.2f}</div>
                            <div class='keywords-found'>
                                {self._generate_keywords_html(point_analysis.get("keywords_found", {}))}
                            </div>
                        </div>
                    </div>
                </div>
            """)

        html_parts.extend([
            "</div>",
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)

    def _generate_keywords_html(self, keywords_found: Dict[str, bool]) -> str:
        """Generate HTML for keywords display."""
        return "".join(
            f"<span class='keyword {('found' if found else '')}'>{keyword}</span>"
            for keyword, found in keywords_found.items()
        )

    def get_prompt(self, lang: str = 'en') -> str:
        """Generate analysis prompt for the Eight-Point Arc."""
        if lang == 'ru':
            prompt_parts = [
                "Проанализируйте следующую нарративную структуру на основе восьмиточечной арки Найджела Уоттса:\n"
            ]
        else:
            prompt_parts = [
                "Analyze the following narrative structure based on Nigel Watts' Eight-Point Arc:\n"
            ]

        current_phase = None
        for point in self.POINTS:
            if point.phase != current_phase:
                current_phase = point.phase
                phase_name = self.PHASE_NAMES[lang][current_phase]
                prompt_parts.append(f"\n{phase_name}:")
            
            point_name = point.name if lang == 'en' else point.name_ru
            point_desc = point.description if lang == 'en' else point.description_ru
            keywords = point.keywords if lang == 'en' else point.keywords_ru
            
            desc_label = "Описание" if lang == 'ru' else "Description"
            importance_label = "Важность" if lang == 'ru' else "Importance"
            elements_label = "Ключевые элементы" if lang == 'ru' else "Key elements to look for"
            
            prompt_parts.extend([
                f"\n{point.number}. {point_name}",
                f"   {desc_label}: {point_desc}",
                f"   {importance_label}: {point.importance}/10",
                f"   {elements_label}:",
                "   " + ", ".join(keywords)
            ])

        return "\n".join(prompt_parts)