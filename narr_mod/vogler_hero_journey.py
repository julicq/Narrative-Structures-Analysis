# narr_mod/vogler_hero_journey.py

from dataclasses import dataclass
import math
from typing import List, Dict, Optional, Final, ClassVar
from enum import Enum
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

class WorldType(Enum):
    ORDINARY = "Ordinary World"
    SPECIAL = "Special World"

class ActType(Enum):
    BEGINNING = "Beginning"
    MIDDLE = "Middle"
    END = "End"

@dataclass
class StageElement:
    name: str
    name_en: str
    description: str
    description_en: str
    keywords: List[str]
    keywords_en: List[str]
    importance: int  # 1-10
    world_type: WorldType

@dataclass
class Stage:
    number: int
    name: str
    name_en: str
    description: str
    description_en: str
    act: ActType
    world: WorldType
    elements: List[StageElement]
    angle: int  # угол на круговой диаграмме
    color: str

@dataclass
class StageAnalysis:
    elements_present: Dict[str, bool]
    strengths: List[str]
    weaknesses: List[str]
    score: float

class VoglerHeroJourney(NarrativeStructure):
    """Implementation of Chris Vogler's Hero's Journey structure."""

    @property
    def structure_type(self) -> StructureType:
        return StructureType.VOGLER_HERO_JOURNEY

    TOTAL_STAGES: Final[int] = 12
    CIRCLE_DEGREES: Final[int] = 360

    STAGES: ClassVar[List[Stage]] = [
        Stage(
            1,
            "Обычный мир",
            "Ordinary World",
            "Начальная точка героя",
            "Hero's starting point",
            ActType.BEGINNING,
            WorldType.ORDINARY,
            [
                StageElement(
                    "Начальное состояние",
                    "Initial State",
                    "Жизнь героя до приключения",
                    "Hero's life before the adventure",
                    ["обычный", "рутина", "повседневный", "будни"],
                    ["normal", "routine", "ordinary", "everyday"],
                    9,
                    WorldType.ORDINARY
                ),
                StageElement(
                    "Установление характера",
                    "Character Establishment",
                    "Представление характера героя",
                    "Introduction of hero's character",
                    ["личность", "черты", "происхождение", "жизнь"],
                    ["personality", "traits", "background", "life"],
                    8,
                    WorldType.ORDINARY
                )
            ],
            0,
            "#e6f3ff"
        ),
        # ... добавьте остальные стадии аналогично
    ]

    WORLD_NAMES = {
        'ru': {
            WorldType.ORDINARY: "Обычный мир",
            WorldType.SPECIAL: "Особый мир"
        },
        'en': {
            WorldType.ORDINARY: "Ordinary World",
            WorldType.SPECIAL: "Special World"
        }
    }

    ACT_NAMES = {
        'ru': {
            ActType.BEGINNING: "Начало",
            ActType.MIDDLE: "Середина",
            ActType.END: "Конец"
        },
        'en': {
            ActType.BEGINNING: "Beginning",
            ActType.MIDDLE: "Middle",
            ActType.END: "End"
        }
    }

    CSS_TEMPLATE: ClassVar[str] = """
        .vogler-journey {
            width: 800px;
            height: 800px;
            position: relative;
            margin: 50px auto;
        }
        .journey-circle {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 3px solid #333;
            position: absolute;
            background: radial-gradient(circle, #fff, #f5f5f5);
        }
        .stage {
            position: absolute;
            width: 120px;
            text-align: center;
            left: 50%;
            top: 50%;
            font-size: 14px;
            line-height: 1.3;
            transform-origin: 0 0;
            transition: all 0.3s ease;
        }
        .stage-content {
            background: rgba(255, 255, 255, 0.9);
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stage-content:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .stage-number {
            font-weight: bold;
            color: #666;
        }
        .stage-name {
            font-weight: bold;
            margin: 5px 0;
        }
        .stage-description {
            font-size: 12px;
            color: #666;
        }
        .world-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
        }
        .ordinary-world {
            background-color: #4CAF50;
        }
        .special-world {
            background-color: #2196F3;
        }
        .connection-line {
            position: absolute;
            height: 2px;
            background: #ddd;
            transform-origin: 0 0;
        }
    """

    def analyze(self, text: str, lang: str = 'en') -> AnalysisResult:
        """
        Analyze the narrative structure according to Vogler's Hero's Journey.
        
        Args:
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            AnalysisResult: Analysis results with detailed evaluation
        """
        formatted_structure = self._split_into_stages(text)
        
        analysis = {
            "stages": {},
            "worlds": {
                "ordinary": self._analyze_world(WorldType.ORDINARY, formatted_structure, lang),
                "special": self._analyze_world(WorldType.SPECIAL, formatted_structure, lang)
            }
        }

        for stage in self.STAGES:
            analysis["stages"][stage.name if lang == 'ru' else stage.name_en] = \
                self._analyze_stage(stage, formatted_structure, lang)

        analysis["overall"] = self._analyze_overall_structure(formatted_structure, lang)

        metadata = AnalysisMetadata(
            model_name="gpt-4",
            model_version="1.0",
            confidence=0.85,
            processing_time=1.0,
            structure_type=self.structure_type,
            display_name=self.display_name
        )

        summary = ("Анализ повествования по методу путешествия героя Воглера" 
                  if lang == 'ru' else 
                  "Analysis of narrative using Vogler's Hero's Journey")

        visualization = self.visualize(analysis, lang)

        return AnalysisResult(
            structure=analysis,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )

    def _split_into_stages(self, text: str) -> Dict[str, str]:
        """Split the text into stages based on keywords and structure."""
        stages_content = {}
        total_length = len(text)
        stage_length = total_length // self.TOTAL_STAGES
        
        for i, stage in enumerate(self.STAGES):
            start = i * stage_length
            end = (i + 1) * stage_length if i < self.TOTAL_STAGES - 1 else total_length
            stage_key = stage.name_en.lower().replace(" ", "_")
            stages_content[stage_key] = text[start:end]
            
        return stages_content

    def _analyze_stage(self, stage: Stage, content: dict, lang: str = 'en') -> StageAnalysis:
        """Analyze a single stage of the journey."""
        stage_content = content.get(stage.name_en.lower().replace(" ", "_"), "")
        
        elements_present = {}
        strengths = []
        weaknesses = []
        
        for element in stage.elements:
            keywords = element.keywords if lang == 'ru' else element.keywords_en
            element_name = element.name if lang == 'ru' else element.name_en
            
            is_present = any(keyword in stage_content.lower() for keyword in keywords)
            elements_present[element_name] = is_present
            
            if is_present:
                strengths.append(
                    f"{element_name} хорошо представлен" if lang == 'ru'
                    else f"{element_name} is well established"
                )
            else:
                weaknesses.append(
                    f"{element_name} требует доработки" if lang == 'ru'
                    else f"{element_name} needs more development"
                )

        return StageAnalysis(
            elements_present=elements_present,
            strengths=strengths,
            weaknesses=weaknesses,
            score=sum(elements_present.values()) / len(stage.elements)
        )

    def _analyze_world(self, world_type: WorldType, content: dict, lang: str = 'en') -> dict:
        """Analyze the representation of a world type."""
        relevant_stages = [s for s in self.STAGES if s.world == world_type]
        world_content = " ".join(content.get(s.name_en.lower().replace(" ", "_"), "") 
                               for s in relevant_stages)
        
        return {
            "strength": len(world_content) / 1000,
            "balance": len(relevant_stages) / len(self.STAGES),
            "transitions": self._analyze_transitions(world_type, content, lang)
        }

    def _analyze_transitions(self, world_type: WorldType, content: dict, lang: str = 'en') -> dict:
        metrics = {
            "clarity": 0.8,
            "impact": 0.7,
            "smoothness": 0.9
        }
        
        if lang == 'ru':
            return {
                "ясность": metrics["clarity"],
                "влияние": metrics["impact"],
                "плавность": metrics["smoothness"]
            }
        return metrics

    def _analyze_overall_structure(self, content: dict, lang: str = 'en') -> dict:
        metrics = {
            "completeness": sum(stage.score for stage in self._get_stage_analyses(content, lang)) / len(self.STAGES),
            "balance": self._analyze_world_balance(content),
            "flow": self._analyze_narrative_flow(content)
        }
        
        if lang == 'ru':
            return {
                "полнота": metrics["completeness"],
                "баланс": metrics["balance"],
                "течение": metrics["flow"]
            }
        return metrics

    def visualize(self, analysis_result: dict, lang: str = 'en') -> str:
        """Generate HTML visualization of the Hero's Journey."""
        title = "Путешествие героя" if lang == 'ru' else "Hero's Journey"
        html_parts = [
            f"<h2>{title}</h2>",
            "<div class='vogler-journey'>",
            "<div class='journey-circle'>"
        ]

        for stage in self.STAGES:
            angle = stage.angle
            radius = 400
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            
            stage_name = stage.name if lang == 'ru' else stage.name_en
            stage_desc = stage.description if lang == 'ru' else stage.description_en
            stage_analysis = analysis_result.get("stages", {}).get(stage_name, {})
            score = stage_analysis.get("score", 0)
            
            html_parts.append(f"""
                <div class='stage' style='
                    transform: translate({x}px, {y}px) rotate({angle}deg);
                    background-color: {self._get_color_by_score(score)};
                '>
                    <div class='stage-content'>
                        <div class='stage-number'>{stage.number}</div>
                        <div class='stage-name'>{stage_name}</div>
                        <div class='world-indicator {stage.world.name.lower()}-world'></div>
                        <div class='stage-description'>{stage_desc}</div>
                    </div>
                </div>
            """)

        html_parts.extend([
            "</div>",
            "</div>",
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)

    def _get_color_by_score(self, score: float) -> str:
        """Generate color based on analysis score."""
        green = int(score * 255)
        return f"rgb(200, {green}, 200)"

    def get_prompt(self, lang: str = 'en') -> str:
        """Generate analysis prompt for the Hero's Journey."""
        if lang == 'ru':
            prompt_parts = [
                "Проанализируйте следующую нарративную структуру на основе 'Путешествия героя' Кристофера Воглера:\n"
            ]
        else:
            prompt_parts = [
                "Analyze the following narrative structure based on Chris Vogler's Hero's Journey:\n"
            ]

        current_act = None
        current_world = None
        
        for stage in self.STAGES:
            if stage.act != current_act:
                current_act = stage.act
                act_name = self.ACT_NAMES[lang][current_act]
                prompt_parts.append(f"\n{act_name}:")
            
            if stage.world != current_world:
                current_world = stage.world
                world_name = self.WORLD_NAMES[lang][current_world]
                prompt_parts.append(f"\n{world_name}:")
            
            stage_name = stage.name if lang == 'ru' else stage.name_en
            stage_desc = stage.description if lang == 'ru' else stage.description_en
            
            prompt_parts.append(f"\n{stage.number}. {stage_name}")
            prompt_parts.append(f"   {stage_desc}")
            
            for element in stage.elements:
                element_name = element.name if lang == 'ru' else element.name_en
                importance_text = "Важность" if lang == 'ru' else "Importance"
                prompt_parts.append(
                    f"   - {element_name} ({importance_text}: {element.importance}/10)"
                )

        return "\n".join(prompt_parts)
    
    def _get_stage_analyses(self, content: dict, lang: str = 'en') -> List[StageAnalysis]:
        return [self._analyze_stage(stage, content, lang) for stage in self.STAGES]

    def _analyze_world_balance(self, content: dict) -> float:
        """Analyze the balance between ordinary and special worlds."""
        ordinary_world = self._analyze_world(WorldType.ORDINARY, content)
        special_world = self._analyze_world(WorldType.SPECIAL, content)
        
        # Вычисляем баланс как отношение меньшего к большему
        return min(ordinary_world["strength"], special_world["strength"]) / \
               max(ordinary_world["strength"], special_world["strength"])

    def _analyze_narrative_flow(self, content: dict, lang: str = 'en') -> float:
        """
        Analyze the narrative flow between stages.
        
        Args:
            content: Dictionary containing stage content
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            float: Flow score between 0 and 1
        """
        # Анализируем переходы между стадиями
        transitions = []
        stage_keys = list(content.keys())
        
        for i in range(len(stage_keys) - 1):
            current_stage = content[stage_keys[i]]
            next_stage = content[stage_keys[i + 1]]
            
            # Проверяем связность между стадиями
            transition_score = self._analyze_stage_transition(
                current_stage, 
                next_stage,
                self.STAGES[i],
                self.STAGES[i + 1],
                lang
            )
            transitions.append(transition_score)
        
        # Возвращаем среднюю оценку переходов
        return sum(transitions) / len(transitions) if transitions else 0.85

    def _analyze_stage_transition(
        self, 
        current_content: str, 
        next_content: str, 
        current_stage: Stage, 
        next_stage: Stage,
        lang: str
    ) -> float:
        """
        Analyze transition between two stages.
        
        Args:
            current_content: Content of current stage
            next_content: Content of next stage
            current_stage: Current stage object
            next_stage: Next stage object
            lang: Language for analysis
            
        Returns:
            float: Transition score between 0 and 1
        """
        # Проверяем ключевые слова текущей и следующей стадии
        current_keywords = []
        next_keywords = []
        
        for element in current_stage.elements:
            current_keywords.extend(
                element.keywords if lang == 'ru' else element.keywords_en
            )
        
        for element in next_stage.elements:
            next_keywords.extend(
                element.keywords if lang == 'ru' else element.keywords_en
            )
        
        # Проверяем наличие связующих элементов
        transition_markers = set(current_keywords) & set(next_keywords)
        transition_strength = len(transition_markers) / \
                            max(len(current_keywords), len(next_keywords))
        
        # Учитываем плавность перехода между мирами
        world_transition_penalty = 0.0
        if current_stage.world != next_stage.world:
            world_transition_penalty = 0.2
        
        return min(1.0, max(0.0, transition_strength - world_transition_penalty))

    def get_stage_name(self, stage_number: int, lang: str = 'en') -> str:
        """
        Get stage name by number in specified language.
        
        Args:
            stage_number: Stage number (1-12)
            lang: Language code ('en' or 'ru')
            
        Returns:
            str: Stage name in specified language
        """
        if 1 <= stage_number <= len(self.STAGES):
            stage = self.STAGES[stage_number - 1]
            return stage.name if lang == 'ru' else stage.name_en
        return ""

    def get_stage_description(self, stage_number: int, lang: str = 'en') -> str:
        """
        Get stage description by number in specified language.
        
        Args:
            stage_number: Stage number (1-12)
            lang: Language code ('en' or 'ru')
            
        Returns:
            str: Stage description in specified language
        """
        if 1 <= stage_number <= len(self.STAGES):
            stage = self.STAGES[stage_number - 1]
            return stage.description if lang == 'ru' else stage.description_en
        return ""

    def get_world_name(self, world_type: WorldType, lang: str = 'en') -> str:
        """
        Get world name in specified language.
        
        Args:
            world_type: WorldType enum value
            lang: Language code ('en' or 'ru')
            
        Returns:
            str: World name in specified language
        """
        return self.WORLD_NAMES[lang][world_type]

    def get_act_name(self, act_type: ActType, lang: str = 'en') -> str:
        """
        Get act name in specified language.
        
        Args:
            act_type: ActType enum value
            lang: Language code ('en' or 'ru')
            
        Returns:
            str: Act name in specified language
        """
        return self.ACT_NAMES[lang][act_type]
