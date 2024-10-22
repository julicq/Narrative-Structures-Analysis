# service/evaluator.py

from narr_mod import get_narrative_structure
from .extractor import extract_structure
from .converter import convert_to_format


def evaluate_narrative(text, structure_name, llm):
    structure = extract_structure(text)
    formatted_structure = convert_to_format(structure, structure_name)
    
    NarrativeStructureClass = get_narrative_structure(structure_name)
    narrative_structure = NarrativeStructureClass()
    
    prompt = narrative_structure.get_prompt().format(**formatted_structure)
    llm_evaluation = llm(prompt)
    
    structure_analysis = narrative_structure.analyze(formatted_structure)
    visualization = narrative_structure.visualize(structure_analysis)
    
    return {
        "structure_name": narrative_structure.name(),
        "llm_evaluation": llm_evaluation,
        "structure_analysis": structure_analysis,
        "visualization": visualization,
        "formatted_structure": formatted_structure,
        "raw_structure": structure
    }
