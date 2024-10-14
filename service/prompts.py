def get_evaluation_prompt(structure_name, formatted_structure):
    base_prompt = f"Оцените следующий текст на соответствие структуре '{structure_name}':\n\n"
    
    for act, content in formatted_structure.items():
        base_prompt += f"{act.upper()}:\n{content['content'][:200]}...\n\n"
    
    base_prompt += "Насколько хорошо этот текст соответствует указанной нарративной структуре? Предоставьте подробный анализ."
    
    return base_prompt
