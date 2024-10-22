# narr_mod/vogler_hero_journey.py

from narr_mod import NarrativeStructure

class VoglerHeroJourney(NarrativeStructure):
    def name(self) -> str:
        return "Путь героя (Крис Воглер)"

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
        html = "<h1>Путь героя (Крис Воглер)</h1>"
        html += "<div class='vogler-journey'>"
        
        stages = [
            ("Обычный мир", "ordinary-world"),
            ("Зов к приключениям", "call-to-adventure"),
            ("Отказ от зова", "refusal"),
            ("Встреча с наставником", "mentor"),
            ("Преодоление порога", "threshold"),
            ("Испытания, союзники, враги", "tests"),
            ("Приближение к пещере", "approach"),
            ("Решающее испытание", "ordeal"),
            ("Награда", "reward"),
            ("Обратный путь", "road-back"),
            ("Воскрешение", "resurrection"),
            ("Возвращение с эликсиром", "return")
        ]
        
        html += "<div class='journey-circle'>"
        for i, (name, class_name) in enumerate(stages):
            angle = i * 30 - 90  # начинаем с -90 градусов (12 часов)
            html += f"<div class='stage {class_name}' style='transform: rotate({angle}deg) translate(150px) rotate(-{angle}deg);'>"
            html += f"<div class='stage-name'>{name}</div>"
            html += "</div>"
        html += "</div>"
        
        html += "<div class='acts'>"
        html += "<div class='act act-1'>Акт 1<br>Отъезд</div>"
        html += "<div class='act act-2-3'>Акт 2 и 3<br>Инициация</div>"
        html += "<div class='act act-4'>Акт 4<br>Возвращение</div>"
        html += "</div>"
        
        html += "</div>"
        
        html += "<style>"
        html += """
            .vogler-journey {
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                font-family: Arial, sans-serif;
                position: relative;
            }
            .journey-circle {
                width: 300px;
                height: 300px;
                border-radius: 50%;
                border: 2px solid #333;
                margin: 0 auto;
                position: relative;
            }
            .stage {
                position: absolute;
                width: 80px;
                height: 80px;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                font-size: 12px;
            }
            .stage-name {
                background-color: #f0f0f0;
                padding: 5px;
                border-radius: 5px;
            }
            .acts {
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
            }
            .act {
                text-align: center;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
                flex: 1;
                margin: 0 5px;
            }
        """
        html += "</style>"
        
        return html

# Создаем экземпляр класса для использования
vogler_hero_journey = VoglerHeroJourney()
