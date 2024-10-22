# narr_mod/gulino_sequence.py

from narr_mod import NarrativeStructure

class GulinoSequence(NarrativeStructure):
    def name(self) -> str:
        return "Последовательный подход (Пол Гулино)"

    def analyze(self, formatted_structure: dict) -> dict:
        # Здесь можно добавить более сложную логику анализа
        # Пока что просто вернем входные данные
        return formatted_structure

    def get_prompt(self) -> str:
        return """
        Analyze the following narrative structure based on Paul Gulino's Sequence Approach:

        Act 1 - Beginning:
        1. Introduction
        2. Stating the Goal
        3. Presenting the Mystery
        4. Heightening Viewer Curiosity
        5. Reaction to the Event
        6. Emergence of a Major Problem

        Act 2 & 3 - Middle:
        7. Hero's Attempt to Solve the Problem: First Try
        8. Probability of Actually Solving the Problem
        9. Introduction of New Characters and Subplots
        10. Rethinking the Main Tension: Calm Before the Storm

        Act 4 - End:
        11. Raised Stakes
        12. Accelerated Pace
        13. "All Is Lost" Moment
        14. Final Resolution, Triggered by a Powerful Twist

        Evaluate how well this narrative follows Paul Gulino's Sequence Approach. 
        Provide insights on the strengths and weaknesses of each element and act, and suggest improvements.
        Consider the following aspects:

        1. How effectively does the Introduction set up the story world and characters?
        2. Is the Goal clearly stated and compelling?
        3. How intriguing is the Mystery presented, and does it engage the audience?
        4. Does the narrative successfully heighten viewer curiosity?
        5. Is the Reaction to the Event believable and impactful?
        6. How significant is the Major Problem that emerges?
        7. Is the Hero's first attempt to solve the problem logical and interesting?
        8. Does the narrative create a sense of possibility for solving the problem?
        9. How well are new characters and subplots integrated into the main story?
        10. Is the "calm before the storm" effectively used to build tension?
        11. How effectively are the stakes raised in the final act?
        12. Does the accelerated pace create a sense of urgency?
        13. Is the "All Is Lost" moment impactful and believable?
        14. How satisfying and surprising is the final resolution and twist?

        Analyze the pacing and balance between the acts. Are there any elements that feel underdeveloped or overly emphasized?
        Suggest how the narrative could be improved to better fit Gulino's Sequence Approach.
        """

    def visualize(self, analysis_result: dict) -> str:
        html = "<h1>Последовательный подход (Пол Гулино)</h1>"
        html += "<div class='gulino-approach'>"
        
        elements = [
            ("Введение", "introduction"),
            ("Указание цели", "stating-goal"),
            ("Загадка", "mystery"),
            ("Усиление любопытства", "heighten-curiosity"),
            ("Реакция на событие", "event-reaction"),
            ("Возникновение проблемы", "problem-emergence"),
            ("Первая попытка", "first-attempt"),
            ("Вероятность решения", "solution-probability"),
            ("Новые герои и подсюжеты", "new-characters-subplots"),
            ("Переосмысление напряжения", "tension-rethinking"),
            ("Повышенные ставки", "raised-stakes"),
            ("Ускоренный темп", "accelerated-pace"),
            ("Момент «все потеряно»", "all-is-lost"),
            ("Финальное решение", "final-resolution")
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
            .gulino-approach {
                width: 100%;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            .timeline {
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                height: 300px;
                margin-bottom: 20px;
            }
            .element {
                width: 7%;
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .element-number {
                background-color: #e74c3c;
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
                font-size: 11px;
                margin-top: 10px;
            }
            .introduction, .final-resolution { height: 40%; }
            .stating-goal, .mystery, .heighten-curiosity, .event-reaction, .problem-emergence { height: 60%; }
            .first-attempt, .solution-probability, .new-characters-subplots, .tension-rethinking { height: 80%; }
            .raised-stakes, .accelerated-pace, .all-is-lost { height: 100%; }
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
            .act-1 { width: 40%; }
            .act-2-3 { width: 35%; }
            .act-4 { width: 25%; }
        """
        html += "</style>"
        
        return html