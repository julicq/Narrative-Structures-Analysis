# narr_mod/campbell_monomyth.py

from dataclasses import dataclass
from typing import Final, ClassVar
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

@dataclass
class MonomythStage:
    name: str
    name_en: str  # Добавляем английское название
    description: str
    description_ru: str  # Добавляем русское описание
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

    # Словарь фаз на разных языках
    PHASES_DICT: ClassVar[dict[str, dict[str, str]]] = {
        'ru': {
            SEPARATION: "Отделение",
            INITIATION: "Инициация",
            RETURN: "Возвращение"
        },
        'en': {
            SEPARATION: "Separation",
            INITIATION: "Initiation",
            RETURN: "Return"
        }
    }

        # Определение стадий мономифа
    STAGES: ClassVar[list[MonomythStage]] = [
        MonomythStage(
            name="Обычный мир",
            name_en="Ordinary World",
            description="The ordinary world before the adventure",
            description_ru="Привычный мир героя до начала приключения",
            phase=SEPARATION
        ),
        MonomythStage(
            name="Зов к приключениям",
            name_en="Call to Adventure",
            description="The call that begins the adventure",
            description_ru="Призыв, с которого начинается приключение",
            phase=SEPARATION
        ),
        MonomythStage(
            name="Отказ от зова",
            name_en="Refusal of the Call",
            description="The hero's initial reluctance or fear",
            description_ru="Первоначальное сопротивление или страх героя",
            phase=SEPARATION
        ),
        MonomythStage(
            name="Встреча с наставником",
            name_en="Meeting with the Mentor",
            description="Finding a mentor who prepares the hero",
            description_ru="Встреча с наставником, который готовит героя",
            phase=SEPARATION
        ),
        MonomythStage(
            name="Преодоление первого порога",
            name_en="Crossing the First Threshold",
            description="The first major challenge or decision",
            description_ru="Первое серьезное испытание или решение",
            phase=SEPARATION
        ),
        MonomythStage(
            name="Испытания, союзники, враги",
            name_en="Tests, Allies and Enemies",
            description="The hero faces various challenges and meets others",
            description_ru="Герой сталкивается с различными испытаниями и встречает других персонажей",
            phase=INITIATION
        ),
        MonomythStage(
            name="Приближение к сокровенному убежищу",
            name_en="Approach to the Inmost Cave",
            description="Preparing for the major challenge",
            description_ru="Подготовка к главному испытанию",
            phase=INITIATION
        ),
        MonomythStage(
            name="Решающее испытание",
            name_en="The Ordeal",
            description="The central life-or-death crisis",
            description_ru="Центральный кризис между жизнью и смертью",
            phase=INITIATION
        ),
        MonomythStage(
            name="Награда",
            name_en="The Reward",
            description="The hero's achievement of the goal",
            description_ru="Достижение героем своей цели",
            phase=INITIATION
        ),
        MonomythStage(
            name="Путь назад",
            name_en="The Road Back",
            description="Beginning the return journey",
            description_ru="Начало обратного пути",
            phase=RETURN
        ),
        MonomythStage(
            name="Воскрешение",
            name_en="Resurrection",
            description="The final test and rebirth",
            description_ru="Финальное испытание и возрождение",
            phase=RETURN
        ),
        MonomythStage(
            name="Возвращение с эликсиром",
            name_en="Return with the Elixir",
            description="Bringing back the prize or lesson",
            description_ru="Возвращение с наградой или уроком",
            phase=RETURN
        ),
    ]

    # Двуязычные шаблоны промптов
    PROMPT_TEMPLATES: ClassVar[dict[str, str]] = {
        'en': """
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
        """,
        
        'ru': """
        Проанализируйте следующую нарративную структуру на основе "Мономифа" Джозефа Кэмпбелла (Путешествие героя):

        Акт 1 - Начало (Отделение):
        - Зов к приключениям
        - Отказ от зова
        - Сверхъестественная помощь
        - Пересечение первого порога

        Акты 2 и 3 - Середина (Инициация):
        - Чрево кита
        - Дорога испытаний
        - Встреча с богиней
        - Женщина как искусительница
        - Примирение с отцом
        - Апофеоз
        - Высшее благо
        - Отказ от возвращения
        - Волшебное бегство

        Акт 4 - Конец (Возвращение):
        - Спасение извне
        - Пересечение порога возвращения
        - Владыка двух миров
        - Свобода жить

        Критерии оценки:
        1. Насколько хорошо история отражает три основные фазы: {phases}?
        2. Прослеживается ли трансформация героя на протяжении путешествия?
        3. Насколько эффективно включены сверхъестественные элементы?
        4. Достаточно ли значимы испытания и трудности?
        5. Демонстрирует ли фаза возвращения рост героя?

        Пожалуйста, проанализируйте темп и баланс между актами, отметьте недостаточно развитые или чрезмерно акцентированные этапы.
        Предложите улучшения для лучшего соответствия структуре Кэмпбелла.
        """
    }

    def get_prompt(self, lang: str = 'en') -> str:
        """
        Generate the analysis prompt for the Monomyth structure in specified language.
        
        Args:
            lang: Language code ('en' or 'ru')
            
        Returns:
            str: Prompt text in specified language
        """
        if lang not in ['en', 'ru']:
            lang = 'en'  # fallback to English
            
        phases = ", ".join([self.PHASES_DICT[lang][phase] for phase in [self.SEPARATION, self.INITIATION, self.RETURN]])
        return self.PROMPT_TEMPLATES[lang].format(phases=phases)

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

    def analyze(self, text: str, lang: str = 'en') -> AnalysisResult:
        """
        Analyze the narrative structure according to Campbell's Monomyth.
        
        Args:
            text: Input text to analyze
            lang: Language for analysis ('en' or 'ru')
            
        Returns:
            AnalysisResult: Analysis results with phases and stages evaluation
        """
        structure = {
            "phases": {
                self.PHASES_DICT[lang][self.SEPARATION]: [],
                self.PHASES_DICT[lang][self.INITIATION]: [],
                self.PHASES_DICT[lang][self.RETURN]: []
            },
            "stages": {
                stage.name if lang == 'ru' else stage.name_en: {} 
                for stage in self.STAGES
            },
            "overall_evaluation": {}
        }
        
        metadata = AnalysisMetadata(
            model_name="gpt-4",
            model_version="1.0",
            confidence=0.85,
            processing_time=1.0,
            structure_type=self.structure_type,
            display_name=self.display_name
        )
        
        summary = ("Анализ нарративной структуры по методу мономифа Кэмпбелла" 
                  if lang == 'ru' else 
                  "Analysis of narrative structure using Campbell's Monomyth")
        
        visualization = self.visualize(structure, lang)
        
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

    def visualize(self, analysis_result: dict, lang: str = 'en') -> str:
        """
        Generate HTML visualization of the Monomyth structure.
        
        Args:
            analysis_result: Dictionary containing analysis results
            lang: Language for visualization ('en' or 'ru')
            
        Returns:
            str: HTML representation of the Monomyth wheel
        """
        title = "Мономиф (Джозеф Кэмпбелл)" if lang == 'ru' else "Monomyth (Joseph Campbell)"
        
        html_parts = [
            f"<h1>{title}</h1>",
            "<div id='monomyth-container'>",
            "<div id='monomyth-circle'></div>"
        ]

        for i, stage in enumerate(self.STAGES):
            stage_name = stage.name if lang == 'ru' else stage.name_en
            stage_div = f"<div class='stage' style='--i:{i};'>{stage_name}</div>"
            html_parts.append(stage_div)

        html_parts.append("</div>")
        html_parts.append(f"<style>{self.CSS_TEMPLATE}</style>")

        return "\n".join(html_parts)

        # Добавляем стили
        html_parts.append(f"<style>{self.CSS_TEMPLATE}</style>")

        return "\n".join(html_parts)
