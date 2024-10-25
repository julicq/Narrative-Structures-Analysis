# service/evaluator.py

import logging
from app.constants import STRUCTURE_MAPPING
from narr_mod import get_narrative_structure
from .extractor import extract_structure
from .converter import convert_to_format

logger = logging.getLogger(__name__)

class NarrativeEvaluator:
    def __init__(self, llm):
        self.llm = llm

    def classify(self, text):
        prompt = f"""Analyze the following text and determine its narrative structure. 
        Choose from the following options:
        1. Eight Point Arch (Nigel Watts)
        2. Hero's journey (Chris Vogler)
        3. Four-Act Structure
        4. Paradigm (Sid Field)
        5. Three-Act Structure
        6. The Monomyth (Joseph Campbell)
        7. The Structure of Story (Chris Soth)
        8. Story Circle (Dan Harmon)
        9. Consistent Approach (Paul Gulino)

        Provide your answer as a single word: "watts_eight_point_arc", "hero_journey", "three_act", "four_act", "monomyth", "soth_story_structure", "harmon_story_circle", "field_paradigm" or "gulino_sequence".
        If none of these structures fit, return "unknown" - only if there is no REALLY a way to determine the type of structure.

        Text: {text}

        Structure:"""
        
        response = self.llm(prompt)
        structure = response.strip()
        
        logger.info(f"Classifier raw response: {structure}")
        
        if structure in STRUCTURE_MAPPING:
            return structure
        else:
            return "unknown"

    # def evaluate(self, text, structure_name=None):
    #     if structure_name is None:
    #         structure_name = self.classify(text)

    #     structure = extract_structure(text)
    #     formatted_structure = convert_to_format(structure, structure_name)
        
    #     NarrativeStructureClass = get_narrative_structure(structure_name)
    #     narrative_structure = NarrativeStructureClass()
        
    #     # Проверяем, является ли formatted_structure словарем
    #     if not isinstance(formatted_structure, dict):
    #         logger.warning(f"Warning: formatted_structure is not a dict. Type: {type(formatted_structure)}")
    #         formatted_structure = {}  # Создаем пустой словарь, если это не словарь
        
    #     # Безопасное форматирование промпта
    #     prompt = narrative_structure.get_prompt()
    #     try:
    #         formatted_prompt = prompt.format(**formatted_structure)
    #     except KeyError as e:
    #         logger.error(f"KeyError when formatting prompt: {e}")
    #         formatted_prompt = prompt  # Используем оригинальный промпт, если форматирование не удалось
        
    #     llm_evaluation = self.llm(formatted_prompt)
        
    #     structure_analysis = narrative_structure.analyze(formatted_structure)
    #     visualization = narrative_structure.visualize(structure_analysis)
        
    #     return {
    #         "structure_name": narrative_structure.name(),
    #         "llm_evaluation": llm_evaluation,
    #         "structure_analysis": structure_analysis,
    #         "visualization": visualization,
    #         "formatted_structure": formatted_structure,
    #         "raw_structure": structure
    #     }

    def analyze_specific_structure(self, text, structure):
        prompt = f"Analyze the following text according to the {structure} narrative structure. NEVER try to guess what this script is film from! Provide a detailed breakdown of how the text fits or doesn't fit this structure:\n\n{text}"
        response = self.llm(prompt)
        
        # Преобразование названия структуры в ключ для convert_to_format
        structure_key = STRUCTURE_MAPPING.get(structure)
        
        if not structure_key:
            logger.warning(f"Structure not found in mapping: {structure}. Using default structure.")
            structure_key = "three_act"
            structure = "Three-Act Structure"

        NarrativeStructureClass = get_narrative_structure(structure_key)
        narrative_structure = NarrativeStructureClass()
        
        formatted_structure = convert_to_format(response, structure_key)
        structure_analysis = narrative_structure.analyze(formatted_structure)
        visualization = narrative_structure.visualize(structure_analysis)
        
        return {
            "structure": structure,
            "analysis": response,
            "formatted_structure": formatted_structure,
            "structure_analysis": structure_analysis,
            "visualization": visualization
        }
