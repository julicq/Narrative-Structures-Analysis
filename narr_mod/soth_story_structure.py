# narr_mod/soth_story_structure.py

from narr_mod import NarrativeStructure

class SothStoryStructure(NarrativeStructure):
    def name(self) -> str:
        return "Структура истории (Крис Сот)"

    def analyze(self, formatted_structure: dict) -> dict:
        # Здесь можно добавить более сложную логику анализа
        # Пока что просто вернем входные данные
        return formatted_structure

    def get_prompt(self) -> str:
        return """
        Analyze the following narrative structure based on Chris Soth's "Mini-Movie Method":

        Act 1 - Beginning:
        1. Hero's World: Call to Adventure
        2. Meeting the Antagonist
        3. Lazy Hero: Hero is "locked in" with the Antagonist

        Act 2 & 3 - Middle:
        4. First Attempts: Usual problem-solving methods don't work
        5. Moving Forward: A big bold plan fails due to lack of information or hero's flaw
        6. Eye-Opening Trial: Hero decides to change
        7. New Plan: The plan fails spectacularly, all seems lost

        Act 4 - End:
        8. Victory in the Final Battle: The Hero has changed
        9. Hero's World: New equilibrium is achieved

        Evaluate how well this narrative follows Chris Soth's story structure. 
        Provide insights on the strengths and weaknesses of each element and act, and suggest improvements.
        Consider the following aspects:

        1. How well is the Hero's World established, and is the Call to Adventure compelling?
        2. Is the Antagonist introduced effectively, creating a strong conflict?
        3. How does the "locked in" situation push the Hero out of their comfort zone?
        4. Are the First Attempts believable and do they show the Hero's initial limitations?
        5. How impactful is the failure of the big bold plan, and does it reveal the Hero's flaw?
        6. Is the Eye-Opening Trial a strong catalyst for the Hero's change?
        7. How devastating is the failure of the New Plan, and does it set up a powerful final act?
        8. Does the Final Battle demonstrate the Hero's growth and change?
        9. How satisfying is the New Equilibrium in the Hero's World?

        Analyze the pacing and balance between the acts. Are there any elements that feel underdeveloped or overly emphasized?
        Suggest how the narrative could be improved to better fit Soth's story structure.
        """

    def visualize(self, analysis_result: dict) -> str:
        html = "<h1>Структура истории (Крис Сот)</h1>"
        html += "<div class='soth-structure'>"
        
        elements = [
            ("Мир героя: Зов приключений", "call-to-adventure"),
            ("Встреча с антагонистом", "meet-antagonist"),
            ("Герой «заперт» вместе с антагонистом", "locked-in"),
            ("Первые попытки", "first-attempts"),
            ("Большой дерзкий план проваливается", "bold-plan-fails"),
            ("Испытание, открывающее герою глаза", "eye-opening-trial"),
            ("Новый план проваливается", "new-plan-fails"),
            ("Победа в финальной битве", "final-battle"),
            ("Новое равновесие", "new-equilibrium")
        ]
        
        html += "<div class='timeline'>"
        for i, (name, class_name) in enumerate(elements):
            html += f"<div class='element {class_name}'>"
            html += f"<div class='element-number'>{i+1}</div>"
            html += f"<div class='element-name'>{name}</div>"
            html += "</div>"
        html += "</div>"
        
        html += "<div class='acts'>"
        html += "<div class='act act-1'>Акт 1<br>Начало</div>"
        html += "<div class='act act-2-3'>Акт 2 - Акт 3<br>Середина</div>"
        html += "<div class='act act-4'>Акт 4<br>Конец</div>"
        html += "</div>"
        
        html += "</div>"
        
        html += "<style>"
        html += """
            .soth-structure {
                width: 100%;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            .timeline {
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                height: 250px;
                margin-bottom: 20px;
            }
            .element {
                width: 10%;
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .element-number {
                background-color: #3498db;
                color: white;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 5px;
            }
            .element-name {
                transform: rotate(-45deg);
                white-space: nowrap;
                font-size: 12px;
                margin-top: 10px;
            }
            .call-to-adventure, .new-equilibrium { height: 30%; }
            .meet-antagonist, .locked-in { height: 50%; }
            .first-attempts, .bold-plan-fails, .eye-opening-trial, .new-plan-fails { height: 70%; }
            .final-battle { height: 100%; }
            .acts {
                display: flex;
                justify-content: space-between;
            }
            .act {
                text-align: center;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
            .act-1 { width: 25%; }
            .act-2-3 { width: 50%; }
            .act-4 { width: 25%; }
        """
        html += "</style>"
        
        return html

# Создаем экземпляр класса для использования
soth_story_structure = SothStoryStructure()
