# service/evaluator.py

from narr_mod import get_narrative_structure
from .extractor import extract_structure
from .converter import convert_to_format

class NarrativeEvaluator:
    def __init__(self, llm):
        self.llm = llm

    def classify(self, text):
        prompt = """
        Analyze the following text and determine which narrative structure it most closely follows:
        1. Hero's Journey (Campbell)
        2. Three-Act Structure
        3. Four-Act Structure
        4. Field's Paradigm

        Provide your answer as a single word: "hero_journey", "three_act", "four_act", or "field_paradigm".

        Text to analyze:
        {text}
        """
        
        response = self.llm(prompt.format(text=text[:1000]))  # Используем первые 1000 символов для классификации
        
        if "hero_journey" in response.lower():
            return "hero_journey"
        elif "three_act" in response.lower():
            return "three_act"
        elif "four_act" in response.lower():
            return "four_act"
        elif "field_paradigm" in response.lower():
            return "field_paradigm"
        else:
            return "unknown"

    def evaluate(self, text, structure_name=None):
        if structure_name is None:
            structure_name = self.classify(text)

        structure = extract_structure(text)
        formatted_structure = convert_to_format(structure, structure_name)
        
        NarrativeStructureClass = get_narrative_structure(structure_name)
        narrative_structure = NarrativeStructureClass()
        
        prompt = narrative_structure.get_prompt().format(**formatted_structure)
        llm_evaluation = self.llm(prompt)
        
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

    def analyze(self, text):
        structure_name = self.classify(text)
        return self.evaluate(text, structure_name)
