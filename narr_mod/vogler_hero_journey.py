# narr_mod/vogler_hero_journey.py

from narr_mod import NarrativeStructure

class VoglerHeroJourney(NarrativeStructure):
    def name(self) -> str:
        return "Hero's journey (Chris Vogler)"

    def analyze(self, formatted_structure: dict) -> dict:
        # Здесь мы можем добавить логику анализа структуры
        # Пока что просто вернем входные данные
        return formatted_structure

    def get_prompt(self) -> str:
        return """
        Analyze the following narrative structure based on Chris Vogler's "Hero's Journey":

        Act 1 - Beginning (Ordinary World):
        - Ordinary World
        - Call to Adventure
        - Refusal of the Call
        - Meeting with the Mentor

        Separation Process:
        - Limited Awareness
        - Increased Awareness
        - Resistance to Change
        - Overcoming Fear
        - Commitment to Change

        Act 2 & 3 - Middle (Special World):
        - Tests, Allies, Enemies
        - Approach to the Inmost Cave
        - Supreme Ordeal, Death & Rebirth
        - Reward (Seizing the Sword)
        - The Road Back

        Descent and Initiation Crisis:
        - Experiments
        - Preparation for Big Change
        - Big Change
        - Consequences of the Attempt
        - Rededication

        Act 4 - End (Return to Ordinary World):
        - Resurrection (Climax)
        - Return with the Elixir (Denouement)
        - Final Attempt
        - Mastery

        Evaluate how well this narrative follows Chris Vogler's "Hero's Journey" structure. 
        Provide insights on the strengths and weaknesses of each stage and act, and suggest improvements.
        Consider the following aspects:

        1. How well does the story transition between the Ordinary World and the Special World?
        2. Is the character's growth and transformation evident throughout the journey?
        3. Are the stages of Separation, Descent, and Return clearly defined and impactful?
        4. How effective is the Supreme Ordeal in challenging the hero and driving the story forward?
        5. Does the Return with the Elixir provide a satisfying conclusion and demonstrate the hero's growth?

        Also, analyze the pacing and balance between the acts. Are there any stages that feel underdeveloped or overly emphasized?
        Suggest how the narrative could be improved to better fit Vogler's Hero's Journey structure.
        """

    def visualize(self, analysis_result: dict) -> str:
        html = """
        <h1>Путь героя (Крис Воглер)</h1>
        <div id='vogler-container'>
            <div id='vogler-circle'></div>
        """
        
        stages = [
            "Обычный мир",
            "Зов к приключениям",
            "Отказ от зова",
            "Встреча с наставником",
            "Преодоление порога",
            "Испытания, союзники, враги",
            "Приближение к пещере",
            "Решающее испытание",
            "Награда",
            "Обратный путь",
            "Воскрешение",
            "Возвращение с эликсиром"
        ]
        
        for i, stage_name in enumerate(stages):
            html += f"<div class='stage' style='--i:{i};'>{stage_name}</div>"
        
        html += "</div>"
        
        html += """
        <style>
            #vogler-container {
                width: 400px;
                height: 400px;
                position: relative;
                margin: 50px auto;
            }
            #vogler-circle {
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
                transform-origin: 0 200px;
                transform: rotate(calc(30deg * var(--i))) translateY(-200px) rotate(calc(-30deg * var(--i)));
            }
            .stage:hover {
                font-weight: bold;
                z-index: 10;
            }
        </style>

        
        """
        
        return html
