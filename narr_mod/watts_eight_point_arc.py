# narr_mod/watts_eight_point_arc.py

from narr_mod import NarrativeStructure

class WattsEightPointArc(NarrativeStructure):
    def name(self) -> str:
        return "Eight Point Arch (Nigel Watts)"

    def analyze(self, formatted_structure: dict) -> dict:
        # Здесь можно добавить более сложную логику анализа
        # Пока что просто вернем входные данные
        return formatted_structure

    def get_prompt(self) -> str:
        return """
        Analyze the following narrative structure based on Nigel Watts' "Eight-Point Arc":

        Act 1 - Beginning:
        1. Stasis
        2. Trigger

        Act 2 & 3 - Middle:
        3. The Quest
        4. Surprise
        5. Critical Choice
        6. Climax

        Act 4 - End:
        7. Reversal
        8. Resolution

        Evaluate how well this narrative follows Nigel Watts' "Eight-Point Arc" structure. 
        Provide insights on the strengths and weaknesses of each point and act, and suggest improvements.
        Consider the following aspects:

        1. How well does the story establish the initial Stasis and how effectively does the Trigger disrupt it?
        2. Is the Quest clearly defined and does it drive the narrative forward?
        3. How impactful and unexpected is the Surprise element?
        4. Does the Critical Choice feel genuinely pivotal to the story's progression?
        5. Is the Climax satisfying and does it effectively resolve the main conflict?
        6. How well does the Reversal demonstrate the consequences of the Climax?
        7. Does the Resolution provide a satisfying conclusion and show how the world has changed?

        Analyze the pacing and balance between the acts. Are there any points that feel underdeveloped or overly emphasized?
        Suggest how the narrative could be improved to better fit Watts' Eight-Point Arc structure.
        """

    def visualize(self, analysis_result: dict) -> str:
        html = "<h1>Восьмиточечная арка (Найджел Уоттс)</h1>"
        html += "<div class='watts-arc'>"
        
        points = [
            "Стазис",
            "Импульс",
            "Стремление к цели",
            "Неожиданность",
            "Решающий выбор",
            "Кульминация",
            "Обратный путь",
            "Развязка"
        ]
        
        for i, point in enumerate(points):
            html += f"<div class='point point-{i+1}'>"
            html += f"<div class='point-number'>{i+1}</div>"
            html += f"<div class='point-name'>{point}</div>"
            html += "</div>"
        
        html += "</div>"
        
        html += "<style>"
        html += """
            .watts-arc {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
                background-color: #f0f0f0;
                border-radius: 10px;
            }
            .point {
                display: flex;
                align-items: center;
                margin: 10px 0;
                padding: 10px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .point-number {
                width: 30px;
                height: 30px;
                background-color: #007bff;
                color: #fff;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                margin-right: 10px;
            }
            .point-name {
                font-weight: bold;
            }
            .point-5 {
                background-color: #ffc107;
            }
            .point-6 {
                background-color: #dc3545;
                color: #fff;
            }
        """
        html += "</style>"
        
        return html

# Создаем экземпляр класса для использования
watts_eight_point_arc = WattsEightPointArc()
