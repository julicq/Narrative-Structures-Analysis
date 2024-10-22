# narr_mod/vogler_hero_journey.py

from narr_mod import NarrativeStructure

class SothStoryStructure(NarrativeStructure):
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
        # Здесь мы можем добавить логику для создания HTML визуализации
        # Пока что просто вернем базовый HTML
        html = "<h1>Путь героя (Крис Воглер)</h1>"
        html += "<ul>"
        for key, value in analysis_result.items():
            html += f"<li><strong>{key}:</strong> {value}</li>"
        html += "</ul>"
        return html

# Создаем экземпляр класса для использования
vogler_hero_journey = SothStoryStructure()
