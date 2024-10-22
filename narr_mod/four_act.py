# narr_mod/four_act.py

from __future__ import annotations
from narr_mod import NarrativeStructure

class FourAct(NarrativeStructure):
    def name(self) -> str:
        return "Four-Act Structure"


    def analyze(self, formatted_structure: dict) -> dict:
        initial_analysis = self._perform_initial_analysis(formatted_structure)
    
        # Добавляем шаг дополнительной проверки
        double_check_result = self._double_check_analysis(formatted_structure, initial_analysis)
        
        # Объединяем результаты
        final_analysis = {**initial_analysis, "double_check": double_check_result}
        
        return final_analysis
    
    def _perform_initial_analysis(self, formatted_structure: dict) -> dict:
        analysis_result = {}
        
        # Извлекаем содержимое для каждого акта из formatted_structure
        act1_content = formatted_structure.get("act1_setup", "")
        act2_content = formatted_structure.get("act2_complication", "")
        act3_content = formatted_structure.get("act3_development", "")
        act4_content = formatted_structure.get("act4_resolution", "")
        
        # Анализируем каждый акт
        analysis_result["Act1"] = self._analyze_act1(act1_content)
        analysis_result["Act2"] = self._analyze_act2(act2_content)
        analysis_result["Act3"] = self._analyze_act3(act3_content)
        analysis_result["Act4"] = self._analyze_act4(act4_content)
        
        return analysis_result


    def _perform_initial_analysis(self, formatted_structure: dict) -> dict:
        analysis_result = {}
        
        # Извлекаем содержимое для каждого акта из formatted_structure
        act1_content = formatted_structure.get("act1_setup", "")
        act2_content = formatted_structure.get("act2_confrontation", "")
        act3_content = formatted_structure.get("act3_resolution", "")
        
        # Анализируем каждый акт
        analysis_result["Act1"] = self._analyze_act1(act1_content)
        analysis_result["Act2"] = self._analyze_act2(act2_content)
        analysis_result["Act3"] = self._analyze_act3(act3_content)
        
        return analysis_result
    
    def _double_check_analysis(self, formatted_structure: dict, initial_analysis: dict) -> str:
        # Подготовка промпта для LLM
        prompt = self._prepare_double_check_prompt(formatted_structure, initial_analysis)
        
        # Вызов LLM для выполнения дополнительной проверки
        llm_response = self._call_llm(prompt)
        
        # Обработка ответа LLM
        double_check_result = self._process_llm_response(llm_response)
        
        return double_check_result

    def _prepare_double_check_prompt(self, formatted_structure: dict, initial_analysis: dict) -> str:
        prompt = f"""
        Пожалуйста, проведите дополнительную проверку анализа следующей трехактной структуры:

        Исходная структура:
        {formatted_structure}

        Первоначальный анализ:
        {initial_analysis}

        {self.double_check_prompt()}

        На основе этой информации, пожалуйста:
        1. Подтвердите или опровергните первоначальный анализ.
        2. Укажите на любые упущения или неточности в первоначальном анализе.
        3. Предложите улучшения или альтернативные интерпретации, если это необходимо.
        """
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        # Здесь должен быть ваш код для вызова LLM
        # Например, использование OpenAI API или другого сервиса
        # Возвращает ответ от LLM
        pass

    def _process_llm_response(self, llm_response: str) -> str:
        # Обработка ответа от LLM
        # Можно добавить дополнительную логику обработки, если это необходимо
        return llm_response
    
    
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

    def get_prompt(self) -> str:
        base_prompt = """
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
        
        return base_prompt + "\n\n" + self.double_check_prompt()


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