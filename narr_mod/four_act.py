# narr_mod/four_act.py

from __future__ import annotations
from narr_mod import NarrativeStructure

class FourAct(NarrativeStructure):
    def name(self) -> str:
        return "Four-Act Structure"

    def analyze(self, formatted_structure: dict) -> dict:
        return {
            "act1": self._analyze_act1(formatted_structure['act1_setup']),
            "act2": self._analyze_act2(formatted_structure['act2_complication']),
            "act3": self._analyze_act3(formatted_structure['act3_development']),
            "act4": self._analyze_act4(formatted_structure['act4_resolution']),
        }

    def get_prompt(self) -> str:
        return """
        Analyze the following narrative structure based on the Four-Act Structure:

        Act 1 (Setup):
        {act1_setup}

        Act 2 (Complication):
        {act2_complication}

        Act 3 (Development):
        {act3_development}

        Act 4 (Resolution):
        {act4_resolution}

        Evaluate how well this narrative follows the Four-Act Structure. 
        Provide insights on the strengths and weaknesses of each act, and suggest improvements.
        Consider the following points for each act:
        - Act 1: How well does it establish the setting, characters, and initial conflict?
        - Act 2: Does it effectively raise the stakes and introduce new challenges?
        - Act 3: How does it develop the conflict and lead to the climax?
        - Act 4: Does it provide a satisfying resolution and tie up loose ends?
        """

    def visualize(self, analysis_result: dict) -> str:
        return f"""
        <div class="four-act-structure">
            <h2>Four-Act Structure Analysis</h2>
            <div class="act">
                <h3>Act 1: Setup</h3>
                <p>{analysis_result['act1']}</p>
            </div>
            <div class="act">
                <h3>Act 2: Complication</h3>
                <p>{analysis_result['act2']}</p>
            </div>
            <div class="act">
                <h3>Act 3: Development</h3>
                <p>{analysis_result['act3']}</p>
            </div>
            <div class="act">
                <h3>Act 4: Resolution</h3>
                <p>{analysis_result['act4']}</p>
            </div>
        </div>
        """

    def _analyze_act1(self, act1_content: str | list[str]) -> str:
        # Анализ первого акта (Setup)
        # Проверяем, насколько хорошо установлены основные элементы истории
        elements_to_check = ['setting', 'main characters', 'initial conflict']
        analysis = "Act 1 (Setup) Analysis:\n"

        # Преобразуем список в строку, если это необходимо
        if isinstance(act1_content, list):
            act1_content = ' '.join(act1_content)

        for element in elements_to_check:
            if element.lower() in act1_content.lower():
                analysis += f"- {element.capitalize()} is present.\n"
            else:
                analysis += f"- {element.capitalize()} might need more emphasis.\n"

        return analysis



    def _analyze_act2(self, act2_content: str) -> str:
        # Анализ второго акта (Complication)
        # Проверяем наличие новых вызовов и повышение ставок
        analysis = "Act 2 (Complication) Analysis:\n"
        
        if 'challenge' in act2_content.lower() or 'obstacle' in act2_content.lower():
            analysis += "- New challenges or obstacles are introduced.\n"
        else:
            analysis += "- The act might benefit from clearer challenges or obstacles.\n"
        
        if 'stakes' in act2_content.lower():
            analysis += "- The stakes appear to be raised.\n"
        else:
            analysis += "- Consider emphasizing how the stakes are raised.\n"
        
        return analysis

    def _analyze_act3(self, act3_content: str) -> str:
        # Анализ третьего акта (Development)
        # Проверяем развитие конфликта и подготовку к кульминации
        analysis = "Act 3 (Development) Analysis:\n"
        
        if 'conflict' in act3_content.lower() and 'develop' in act3_content.lower():
            analysis += "- The conflict seems to be developing.\n"
        else:
            analysis += "- The conflict development could be more pronounced.\n"
        
        if 'climax' in act3_content.lower():
            analysis += "- The act appears to be building towards a climax.\n"
        else:
            analysis += "- Consider making the build-up to the climax more evident.\n"
        
        return analysis

    def _analyze_act4(self, act4_content: str) -> str:
        # Анализ четвертого акта (Resolution)
        # Проверяем разрешение конфликта и завершение сюжетных линий
        analysis = "Act 4 (Resolution) Analysis:\n"
        
        if 'resolve' in act4_content.lower() or 'resolution' in act4_content.lower():
            analysis += "- The main conflict appears to be resolved.\n"
        else:
            analysis += "- The resolution of the main conflict could be clearer.\n"
        
        if 'conclusion' in act4_content.lower() or 'end' in act4_content.lower():
            analysis += "- The story seems to reach a conclusion.\n"
        else:
            analysis += "- Consider providing a more definitive conclusion.\n"
        
        return analysis
