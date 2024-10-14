# narr_mod/campbell_monomyth.py

from narr_mod import NarrativeStructure

class CampbellMonomyth(NarrativeStructure):
    def name(self) -> str:
        return "Мономиф (Джозеф Кэмпбелл)"

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
        html = "<h1>Мономиф (Джозеф Кэмпбелл)</h1>"
        html += "<div class='monomyth-circle'>"
        
        stages = [
            ("Обычный мир", "ordinary-world"),
            ("Зов к приключениям", "call-to-adventure"),
            ("Отказ от зова", "refusal-of-call"),
            ("Встреча с наставником", "meeting-mentor"),
            ("Преодоление первого порога", "crossing-threshold"),
            ("Испытания, союзники, враги", "tests-allies-enemies"),
            ("Приближение к сокровенному убежищу", "approach-inmost-cave"),
            ("Решающее испытание", "ordeal"),
            ("Награда", "reward"),
            ("Путь назад", "road-back"),
            ("Воскрешение", "resurrection"),
            ("Возвращение с эликсиром", "return-with-elixir")
        ]
        
        for i, (stage_name, stage_class) in enumerate(stages):
            angle = i * 30 - 90  # Start from top (-90 degrees)
            html += f"<div class='stage {stage_class}' style='transform: rotate({angle}deg) translate(150px) rotate(-{angle}deg);'>{stage_name}</div>"
        
        html += "</div>"
        
        html += "<style>"
        html += """
            .monomyth-circle {
                width: 400px;
                height: 400px;
                border-radius: 50%;
                border: 2px solid #333;
                position: relative;
                margin: 50px auto;
            }
            .stage {
                position: absolute;
                width: 100px;
                text-align: center;
                transform-origin: center;
            }
        """
        html += "</style>"
        
        return html

# Создаем экземпляр класса для использования
campbell_monomyth = CampbellMonomyth()
