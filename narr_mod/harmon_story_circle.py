# narr_mod/harmon_story_circle.py

from narr_mod import NarrativeStructure

class HarmonStoryCircle(NarrativeStructure):
    def name(self) -> str:
        return "Сюжетный круг (Дэн Хармон)"

    def analyze(self, formatted_structure: dict) -> dict:
        # Здесь можно добавить более сложную логику анализа
        # Пока что просто вернем входные данные
        return formatted_structure

    def get_prompt(self) -> str:
        return """
        Analyze the following narrative structure based on Dan Harmon's "Story Circle":

        Act 1 - Beginning:
        1. You (Comfort Zone)
        2. Need (Desire)

        Act 2 & 3 - Middle:
        3. Go (Unfamiliar situation)
        4. Search (Adaptation)
        5. Find (Getting what they wanted)
        6. Take (Paying the price)

        Act 4 - End:
        7. Return (Back to familiar situation)
        8. Change (New ability)

        Evaluate how well this narrative follows Dan Harmon's "Story Circle" structure. 
        Provide insights on the strengths and weaknesses of each step and act, and suggest improvements.
        Consider the following aspects:

        1. How well is the protagonist's initial state (Comfort Zone) established?
        2. Is the Need or Desire clearly defined and compelling?
        3. How effectively does the story push the protagonist into an Unfamiliar situation?
        4. Is the Search and Adaptation phase well-developed and challenging?
        5. Does the Find step feel satisfying and earned?
        6. Is there a clear price or consequence for Taking what was found?
        7. How does the Return phase compare to the initial state?
        8. Is the Change in the protagonist evident and meaningful?

        Analyze the pacing and balance between the acts. Are there any steps that feel underdeveloped or overly emphasized?
        Suggest how the narrative could be improved to better fit Harmon's Story Circle structure.
        """

    def visualize(self, analysis_result: dict) -> str:
        html = "<h1>Сюжетный круг (Дэн Хармон)</h1>"
        html += "<div class='harmon-circle'>"
        
        steps = [
            "Зона комфорта",
            "Потребность или желание",
            "Незнакомая ситуация",
            "Поиск и адаптация",
            "Получение желаемого",
            "Плата за него",
            "Возвращение к привычному",
            "Способность меняться"
        ]
        
        for i, step in enumerate(steps):
            angle = i * 45 - 90  # Start from top (-90 degrees)
            html += f"<div class='step step-{i+1}' style='transform: rotate({angle}deg) translate(150px) rotate(-{angle}deg);'>"
            html += f"<div class='step-number'>{i+1}</div>"
            html += f"<div class='step-name'>{step}</div>"
            html += "</div>"
        
        html += "</div>"
        
        html += "<style>"
        html += """
            .harmon-circle {
                width: 400px;
                height: 400px;
                border-radius: 50%;
                border: 2px solid #333;
                position: relative;
                margin: 50px auto;
            }
            .step {
                position: absolute;
                width: 100px;
                text-align: center;
                transform-origin: center;
            }
            .step-number {
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 5px;
            }
            .step-name {
                font-size: 12px;
            }
            .step-1 { color: #e74c3c; }
            .step-2 { color: #3498db; }
            .step-3 { color: #2ecc71; }
            .step-4 { color: #f39c12; }
            .step-5 { color: #9b59b6; }
            .step-6 { color: #e67e22; }
            .step-7 { color: #1abc9c; }
            .step-8 { color: #34495e; }
        """
        html += "</style>"
        
        return html

# Создаем экземпляр класса для использования
harmon_story_circle = HarmonStoryCircle()
