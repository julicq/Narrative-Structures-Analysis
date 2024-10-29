# service/evaluator.py

import logging
from narr_mod import StructureType, get_narrative_structure
from .extractor import extract_structure
from .converter import convert_to_format, StoryStructureConverter

logger = logging.getLogger(__name__)

class NarrativeEvaluator:
    """
    Класс для оценки и анализа нарративных структур текста.
    """
    
    def __init__(self, llm):
        """
        Инициализация оценщика нарративных структур.
        
        Args:
            llm: Модель машинного обучения для анализа текста
        """
        self.llm = llm
        self.structure_converter = StoryStructureConverter()

    def classify(self, text: str) -> str:
        """
        Классифицирует текст по типу нарративной структуры.
        
        Args:
            text: Текст для анализа
            
        Returns:
            str: Определенный тип структуры или "unknown"
        """
        prompt = f"""Analyze the following text and determine its narrative structure. 
        Choose from the following options:
        1. Eight Point Arc (Nigel Watts)
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
        structure = response.strip().lower()
        
        logger.info(f"Classifier raw response: {structure}")
        
        try:
            # Проверяем, является ли структура валидным значением StructureType
            StructureType(structure)
            return structure
        except ValueError:
            return "unknown"

    def evaluate(self, text: str, structure_name: str = None) -> dict:
        """
        Проводит полный анализ текста согласно определенной структуре.
        
        Args:
            text: Текст для анализа
            structure_name: Название структуры (опционально)
            
        Returns:
            dict: Результаты анализа
        """
        if structure_name is None:
            structure_name = self.classify(text)

        # Извлекаем базовую структуру
        structure = extract_structure(text)
        
        # Конвертируем в нужный формат
        formatted_structure = convert_to_format(structure, structure_name)
        
        # Получаем класс для работы с выбранной структурой
        NarrativeStructureClass = get_narrative_structure(structure_name)
        narrative_structure = NarrativeStructureClass()
        
        # Проверяем корректность структуры
        if not isinstance(formatted_structure, dict):
            logger.warning(f"Warning: formatted_structure is not a dict. Type: {type(formatted_structure)}")
            formatted_structure = {}
        
        # Формируем и выполняем промпт
        try:
            prompt = narrative_structure.get_prompt()
            formatted_prompt = prompt.format(**formatted_structure)
            llm_evaluation = self.llm(formatted_prompt)
        except (KeyError, ValueError) as e:
            logger.error(f"Error during prompt formatting and evaluation: {e}")
            llm_evaluation = "Error during evaluation"
        
        # Проводим структурный анализ
        try:
            structure_analysis = narrative_structure.analyze(formatted_structure)
            visualization = narrative_structure.visualize(structure_analysis)
        except Exception as e:
            logger.error(f"Error during structure analysis: {e}")
            structure_analysis = {}
            visualization = None
        
        return {
            "structure_name": narrative_structure.name(),
            "llm_evaluation": llm_evaluation,
            "structure_analysis": structure_analysis,
            "visualization": visualization,
            "formatted_structure": formatted_structure,
            "raw_structure": structure
        }

    def analyze_specific_structure(self, text: str, structure: str) -> dict:
        """
        Анализирует текст согласно конкретной нарративной структуре.
        
        Args:
            text: Текст для анализа
            structure: Название структуры
            
        Returns:
            dict: Результаты анализа
        """
        # Формируем промпт для анализа
        display_name = StructureType.get_display_name(structure)
        prompt = f"""Analyze the following text according to the {display_name} narrative structure. 
        NEVER try to guess what this script is film from! 
        Provide a detailed breakdown of how the text fits or doesn't fit this structure:

        {text}"""
        
        response = self.llm(prompt)
        
        try:
            structure_type = StructureType(structure)
        except ValueError:
            logger.warning(f"Structure not found: {structure}. Using default structure.")
            structure_type = StructureType.THREE_ACT
            structure = structure_type.value

        # Получаем класс структуры и создаем экземпляр
        narrative_structure = get_narrative_structure(structure_type)
        
        # Извлекаем и форматируем структуру
        extracted_structure = extract_structure(text)
        formatted_structure = convert_to_format(extracted_structure, structure)
        
        # Проводим анализ
        try:
            structure_analysis = narrative_structure.analyze(formatted_structure)
            visualization = narrative_structure.visualize(structure_analysis)
        except Exception as e:
            logger.error(f"Error during structure analysis: {e}")
            structure_analysis = {}
            visualization = None
        
        return {
            "structure": display_name,
            "analysis": response,
            "formatted_structure": formatted_structure,
            "structure_analysis": structure_analysis,
            "visualization": visualization
        }

    def get_available_structures(self) -> list:
        """
        Возвращает список доступных структур для анализа.
        
        Returns:
            list: Список структур с описаниями
        """
        return self.structure_converter.get_available_structures()

    def get_structure_info(self, structure_name: str) -> dict:
        """
        Возвращает информацию о конкретной структуре.
        
        Args:
            structure_name: Название структуры
            
        Returns:
            dict: Информация о структуре
        """
        return self.structure_converter.get_structure_info(structure_name)
