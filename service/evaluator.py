from .extractor import extract_structure
from .converter import convert_to_format
from .prompts import get_evaluation_prompt

def evaluate_narrative(text, structure_name, llm):
    structure = extract_structure(text)
    formatted_structure = convert_to_format(structure, structure_name)
    prompt = get_evaluation_prompt(structure_name, formatted_structure)
    
    evaluation = llm(prompt)
    
    return {
        "structure_name": structure_name,
        "evaluation": evaluation,
        "formatted_structure": formatted_structure,
        "raw_structure": structure
    }
