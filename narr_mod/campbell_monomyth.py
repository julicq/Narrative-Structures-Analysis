# narr_mod/campbell_monomyth.py

from dataclasses import dataclass
from typing import Final, ClassVar
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

@dataclass
class MonomythStage:
    name: str
    description: str
    phase: str

class CampbellMonomyth(NarrativeStructure):
    """Implementation of Joseph Campbell's Monomyth (Hero's Journey) structure."""

    # Добавляем реализацию абстрактного метода structure_type
    @property
    def structure_type(self) -> StructureType:
        return StructureType.MONOMYTH
    
    # Константы для фаз
    SEPARATION: Final[str] = "Separation"
    INITIATION: Final[str] = "Initiation"
    RETURN: Final[str] = "Return"

    # Определение стадий мономифа
    STAGES: ClassVar[list[MonomythStage]] = [
        MonomythStage("Обычный мир", "The ordinary world before the adventure", SEPARATION),
        MonomythStage("Зов к приключениям", "The call to adventure", SEPARATION),
        MonomythStage("Отказ от зова", "Refusal of the call", SEPARATION),
        MonomythStage("Встреча с наставником", "Meeting with the mentor", SEPARATION),
        MonomythStage("Преодоление первого порога", "Crossing the first threshold", SEPARATION),
        MonomythStage("Испытания, союзники, враги", "Tests, allies and enemies", INITIATION),
        MonomythStage("Приближение к сокровенному убежищу", "Approach to the inmost cave", INITIATION),
        MonomythStage("Решающее испытание", "The ordeal", INITIATION),
        MonomythStage("Награда", "The reward", INITIATION),
        MonomythStage("Путь назад", "The road back", RETURN),
        MonomythStage("Воскрешение", "Resurrection", RETURN),
        MonomythStage("Возвращение с эликсиром", "Return with the elixir", RETURN),
    ]

    PROMPT_TEMPLATE: ClassVar[str] = """
    Analyze the following narrative structure based on Joseph Campbell's "Monomyth" (The Hero's Journey):

    Act 1 - Beginning (Separation):
    - Call to Adventure
    - Refusal of the Call
    - Supernatural Aid
    - Crossing the First Threshold

    Act 2 & 3 - Middle (Initiation):
    - Belly of the Whale
    - Road of Trials
    - Meeting with the Goddess
    - Woman as Temptress
    - Atonement with the Father
    - Apotheosis
    - The Ultimate Boon
    - Refusal of the Return
    - Magic Flight

    Act 4 - End (Return):
    - Rescue from Without
    - The Crossing of the Return Threshold
    - Master of Two Worlds
    - Freedom to Live

    Evaluation Criteria:
    1. How well does the story represent the three main phases: {phases}?
    2. Is the hero's transformation evident throughout the journey?
    3. How effectively are the supernatural elements incorporated?
    4. Are the challenges and trials sufficiently impactful?
    5. Does the return phase demonstrate the hero's growth?

    Please analyze pacing and balance between acts, noting any underdeveloped or overemphasized stages.
    Provide improvement suggestions to better align with Campbell's structure.
    """

    CSS_TEMPLATE: ClassVar[str] = """
    #monomyth-container {
        width: 400px;
        height: 400px;
        position: relative;
        margin: 50px auto;
    }
    #monomyth-circle {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 2px solid #333;
        position: absolute;
    }
    .stage {
        position: absolute;
        width: 100px;
        text-align: center;
        left: 50%;
        top: 50%;
        font-size: 12px;
        line-height: 1.2;
        transform-origin: 0 300px;
        transform: rotate(calc(30deg * var(--i))) translateY(-300px) rotate(calc(-30deg * var(--i)));
    }
    .stage:hover {
        font-weight: bold;
        color: #0066cc;
        cursor: pointer;
    }
    """

    def analyze(self, text: str) -> AnalysisResult:
        """
        Analyze the narrative structure according to Campbell's Monomyth.
        
        Args:
            text: Input text to analyze
            
        Returns:
            AnalysisResult: Analysis results with phases and stages evaluation
        """
        # В будущем здесь можно добавить более сложную логику анализа
        structure = {
            "phases": {
                self.SEPARATION: [],
                self.INITIATION: [],
                self.RETURN: []
            },
            "stages": {stage.name: {} for stage in self.STAGES},
            "overall_evaluation": {}
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
        summary = "Analysis of narrative structure using Campbell's Monomyth"
        
        # Создаем визуализацию
        visualization = self.visualize(structure)
        
        # Возвращаем результат в правильном формате
        return AnalysisResult(
            structure=structure,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )

    def get_prompt(self) -> str:
        """Generate the analysis prompt for the Monomyth structure."""
        phases = ", ".join([self.SEPARATION, self.INITIATION, self.RETURN])
        return self.PROMPT_TEMPLATE.format(phases=phases)

    def visualize(self, analysis_result: dict) -> str:
        """
        Generate HTML visualization of the Monomyth structure.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            str: HTML representation of the Monomyth wheel
        """
        html_parts = [
            "<h1>Мономиф (Джозеф Кэмпбелл)</h1>",
            "<div id='monomyth-container'>",
            "<div id='monomyth-circle'></div>"
        ]

        # Добавляем стадии
        for i, stage in enumerate(self.STAGES):
            stage_div = f"<div class='stage' style='--i:{i};'>{stage.name}</div>"
            html_parts.append(stage_div)

        # Закрываем контейнер
        html_parts.append("</div>")

        # Добавляем стили
        html_parts.append(f"<style>{self.CSS_TEMPLATE}</style>")

        return "\n".join(html_parts)
