# narr_mod/field_paradigm.py

from narr_mod import NarrativeStructure

class FieldParadigm(NarrativeStructure):
    def name(self) -> str:
        return "Парадигма (Сид Филд)"

    def analyze(self, formatted_structure: dict) -> dict:
        # Здесь можно добавить более сложную логику анализа
        # Пока что просто вернем входные данные
        return formatted_structure

    def get_prompt(self) -> str:
        return """
        Analyze the following narrative structure based on Syd Field's "Paradigm":

        Act 1 - Beginning (Setup):
        1. Inciting Incident
        2. Plot Point 1

        Act 2 - Middle (Confrontation):
        3. Pinch 1
        4. Midpoint
        5. Pinch 2
        6. Plot Point 2

        Act 3 - End (Resolution):
        7. Climax
        8. Resolution

        Evaluate how well this narrative follows Syd Field's "Paradigm" structure. 
        Provide insights on the strengths and weaknesses of each element and act, and suggest improvements.
        Consider the following aspects:

        1. How effectively does the Inciting Incident set up the story?
        2. Is Plot Point 1 a strong turning point that propels the story into Act 2?
        3. How well do Pinch 1 and Pinch 2 maintain tension and drive the story forward?
        4. Does the Midpoint effectively shift the direction or raise the stakes of the story?
        5. Is Plot Point 2 impactful enough to transition into the final act?
        6. How satisfying and logical is the Climax in resolving the main conflict?
        7. Does the Resolution tie up loose ends and provide a satisfying conclusion?

        Analyze the pacing and balance between the acts. Are there any elements that feel underdeveloped or overly emphasized?
        Suggest how the narrative could be improved to better fit Field's Paradigm structure.
        """

    def visualize(self, analysis_result: dict) -> str:
        html = "<h1>Парадигма (Сид Филд)</h1>"
        html += "<div class='field-paradigm'>"
        
        elements = [
            ("Провоцирующее событие", "inciting-incident"),
            ("Сюжетный поворот 1", "plot-point-1"),
            ("Точка фокусировки 1", "pinch-1"),
            ("Мидпоинт", "midpoint"),
            ("Точка фокусировки 2", "pinch-2"),
            ("Сюжетный поворот 2", "plot-point-2"),
            ("Кульминация", "climax"),
            ("Развязка", "resolution")
        ]
        
        html += "<div class='timeline'>"
        for name, class_name in elements:
            html += f"<div class='element {class_name}'>"
            html += f"<div class='element-name'>{name}</div>"
            html += "</div>"
        html += "</div>"
        
        html += "<div class='acts'>"
        html += "<div class='act act-1'>Акт 1<br>Завязка</div>"
        html += "<div class='act act-2'>Акт 2 - Акт 3<br>Противостояние</div>"
        html += "<div class='act act-4'>Акт 4<br>Развязка</div>"
        html += "</div>"
        
        html += "</div>"
        
        html += "<style>"
        html += """
            .field-paradigm {
                width: 100%;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            .timeline {
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                height: 200px;
                margin-bottom: 20px;
            }
            .element {
                width: 10%;
                text-align: center;
            }
            .element-name {
                transform: rotate(-45deg);
                white-space: nowrap;
                font-size: 12px;
            }
            .inciting-incident, .resolution { height: 30%; }
            .plot-point-1, .plot-point-2 { height: 80%; }
            .pinch-1, .pinch-2 { height: 50%; }
            .midpoint { height: 60%; }
            .climax { height: 100%; }
            .acts {
                display: flex;
                justify-content: space-between;
            }
            .act {
                width: 30%;
                text-align: center;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
            .act-2 {
                width: 40%;
            }
        """
        html += "</style>"
        
        return html

# Создаем экземпляр класса для использования
field_paradigm = FieldParadigm()
