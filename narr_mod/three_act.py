# narr_mod/three_act.py

from narr_mod import NarrativeStructure

class ThreeAct(NarrativeStructure):
    def name(self) -> str:
        return "Трехактная структура"

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



    def _analyze_act1(self, act1_content: str) -> str:
        analysis = "Act 1 (Setup) Analysis:\n"
        elements_to_check = ['setting', 'main characters', 'initial conflict']
        
        for element in elements_to_check:
            if element.lower() in act1_content.lower():
                analysis += f"- {element.capitalize()} is present.\n"
            else:
                analysis += f"- {element.capitalize()} might need more emphasis.\n"
        
        return analysis

    def _analyze_act2(self, act2_content: str) -> str:
        analysis = "Act 2 (Confrontation) Analysis:\n"
        
        if 'conflict' in act2_content.lower() and 'develop' in act2_content.lower():
            analysis += "- The conflict seems to be developing.\n"
        else:
            analysis += "- The conflict development could be more pronounced.\n"
        
        if 'stakes' in act2_content.lower():
            analysis += "- The stakes appear to be raised.\n"
        else:
            analysis += "- Consider emphasizing how the stakes are raised.\n"
        
        return analysis

    def _analyze_act3(self, act3_content: str) -> str:
        analysis = "Act 3 (Resolution) Analysis:\n"
        
        if 'resolve' in act3_content.lower() or 'resolution' in act3_content.lower():
            analysis += "- The main conflict appears to be resolved.\n"
        else:
            analysis += "- The resolution of the main conflict could be clearer.\n"
        
        if 'conclusion' in act3_content.lower() or 'end' in act3_content.lower():
            analysis += "- The story seems to reach a conclusion.\n"
        else:
            analysis += "- Consider providing a more definitive conclusion.\n"
        
        return analysis


    def get_prompt(self) -> str:
        base_prompt = """
        Analyze the following narrative structure based on the Three-Act Structure:

        Act 1: Setup
        Act 2: Confrontation
        Act 3: Resolution

        Evaluate how well this narrative follows the Three-Act Structure. 
        Provide insights on the strengths and weaknesses of each act, and suggest improvements.
        Consider the following aspects:

        1. How well does Act 1 establish the setting, characters, and initial conflict?
        2. Does Act 2 effectively develop the conflict and raise the stakes?
        3. Is the resolution in Act 3 satisfying and does it tie up loose ends?

        Analyze the pacing and balance between the acts. Are there any parts that feel underdeveloped or overly emphasized?
        Suggest how the narrative could be improved to better fit the Three-Act Structure.
        """
        
        return base_prompt + "\n\n" + self.double_check_prompt()


    def visualize(self, analysis_result: dict) -> str:
        html = "<h2>Трехактная структура</h2>"
        html += "<div class='three-act-structure'>"
        
        acts = ["Setup", "Confrontation", "Resolution"]
        
        for i, act in enumerate(acts):
            act_content = analysis_result.get(f"Act{i+1}", "")
            html += f"<div class='act act-{i+1}'>"
            html += f"<h3>Act {i+1}: {act}</h3>"
            html += f"<p>{act_content}</p>"
            html += "</div>"
        
        html += "</div>"
        
        html += "<style>"
        html += """
            .three-act-structure {
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
            }
            .act {
                width: 30%;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .act-1 {
                background-color: #e6f3ff;
            }
            .act-2 {
                background-color: #fff2e6;
            }
            .act-3 {
                background-color: #e6ffe6;
            }
            h3 {
                margin-top: 0;
                color: #333;
            }
        """
        html += "</style>"
        
        return html

# Создаем экземпляр класса для использования
three_act_structure = ThreeAct()
