# narr_mod/campbell_monomyth.py

from narr_mod import NarrativeStructure

class CampbellMonomyth(NarrativeStructure):
    def name(self) -> str:
        return "The Monomyth (Joseph Campbell)"

    def analyze(self, formatted_structure: dict) -> dict:
        # Здесь можно добавить более сложную логику анализа
        # Пока что просто вернем входные данные
        return formatted_structure

    def get_prompt(self) -> str:
        return """
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

        Evaluate how well this narrative follows Joseph Campbell's "Monomyth" structure. 
        Provide insights on the strengths and weaknesses of each stage and act, and suggest improvements.
        Consider the following aspects:

        1. How well does the story represent the three main phases: Separation, Initiation, and Return?
        2. Is the hero's transformation evident throughout the journey?
        3. How effectively are the supernatural elements incorporated into the story?
        4. Are the challenges and trials faced by the hero sufficiently impactful and transformative?
        5. Does the return phase demonstrate the hero's growth and the impact of their journey on their world?

        Analyze the pacing and balance between the acts. Are there any stages that feel underdeveloped or overly emphasized?
        Suggest how the narrative could be improved to better fit Campbell's Monomyth structure.
        """

    def visualize(self, analysis_result: dict) -> str:
        html = """
        <h1>Мономиф (Джозеф Кэмпбелл)</h1>
        <div id='monomyth-container'>
            <div id='monomyth-circle'></div>
        """
        
        stages = [
            "Обычный мир",
            "Зов к приключениям",
            "Отказ от зова",
            "Встреча с наставником",
            "Преодоление первого порога",
            "Испытания, союзники, враги",
            "Приближение к сокровенному убежищу",
            "Решающее испытание",
            "Награда",
            "Путь назад",
            "Воскрешение",
            "Возвращение с эликсиром"
        ]
        
        for i, stage_name in enumerate(stages):
            html += f"<div class='stage' style='--i:{i};'>{stage_name}</div>"
        
        html += "</div>"
        
        html += """
        <style>
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
                z-index: 10;
            }
        </style>
        """
        
        return html
