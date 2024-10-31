# service/evaluator.py

import logging
from narr_mod import StructureType, get_narrative_structure
from .extractor import extract_structure
from .converter import convert_to_format, StoryStructureConverter
from typing import Union, Optional
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

logger = logging.getLogger(__name__)

class NarrativeEvaluator:
    """
    Класс для оценки и анализа нарративных структур текста.
    """
    
    def __init__(self, llm, gigachat_token: Optional[str] = None):
        """
        Инициализация оценщика нарративных структур.
        
        Args:
            llm: Основная модель (Ollama)
            gigachat_token: Токен для GigaChat (опционально)
        """
        self.llm = llm
        self.structure_converter = StoryStructureConverter()
        self.gigachat = None
        if gigachat_token:
            try:
                self.gigachat = GigaChat(credentials=gigachat_token)
                logger.info("GigaChat initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize GigaChat: {e}")

    def _call_llm(self, prompt: str) -> str:
        """
        Вызывает LLM с fallback на GigaChat.
        """
        try:
            # Используем .invoke() вместо прямого вызова
            response = self.llm.invoke(prompt)
            # Handle AIMessage or similar objects
            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, str):
                return response
            else:
                return str(response)
        except Exception as e:
            logger.warning(f"Primary LLM failed: {e}")
            if self.gigachat:
                try:
                    messages = [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                    response = self.gigachat.chat(messages)
                    return response.choices[0].message.content
                except Exception as e:
                    logger.error(f"GigaChat also failed: {e}")
                    raise
            else:
                raise


    def classify(self, text: str) -> str:
        """
        Классифицирует текст по типу нарративной структуры.
        
        Args:
            text: Текст для анализа
            
        Returns:
            str: Определенный тип структуры или "unknown"
        """
        prompt = f"""As a screenplay structure expert, analyze this screenplay and determine its narrative structure. 
        Consider the following aspects:
        1. Plot progression and major turning points
        2. Character development arcs
        3. Act structure and scene organization
        4. Key dramatic moments and their placement
        
        Choose the MOST APPROPRIATE structure from these options:
        1. "watts_eight_point_arc" - Eight Point Arc (Nigel Watts)
        - Stasis → Trigger → Quest → Surprise → Critical Choice → Climax → Reversal → Resolution
        
        2. "vogler_hero_journey" - Hero's Journey (Chris Vogler)
        - Ordinary World → Call to Adventure → Refusal → Meeting the Mentor → Crossing the Threshold → Tests, Allies, Enemies → Approach → Ordeal → Reward → Road Back → Resurrection → Return
        
        3. "three_act" - Three-Act Structure
        - Setup (Act 1) → Confrontation (Act 2) → Resolution (Act 3)
        - With clear inciting incident, midpoint, and climax
        
        4. "four_act" - Four-Act Structure
        - Setup → Development → Climax → Resolution
        - Each act approximately 25-30 pages
        
        5. "field_paradigm" - Paradigm (Sid Field)
        - Setup → Plot Point 1 → Confrontation → Plot Point 2 → Resolution
        - Strong emphasis on plot points
        
        6. "monomyth" - The Monomyth (Joseph Campbell)
        - Departure → Initiation → Return
        - Focus on hero's psychological/mythological journey
        
        7. "soth_story_structure" - Mini-Movie Method (Chris Soth)
        - Eight clear 15-minute segments
        - Each segment with its own dramatic arc
        
        8. "harmon_story_circle" - Story Circle (Dan Harmon)
        - You → Need → Go → Search → Find → Take → Return → Change
        
        9. "gulino_sequence" - Sequence Approach (Paul Gulino)
        - Eight 8-15 page sequences
        - Each sequence as a mini-movie

        Analyze the following screenplay excerpt and return ONLY the structure identifier (e.g. "three_act") that best matches. 
        If truly impossible to determine, return "unknown".

        Screenplay:
        {text}

        Structure identifier:"""
        
        try:
            response = self._call_llm(prompt)
            structure = response.strip().lower()
            
            logger.info(f"Classifier raw response: {structure}")
            
            # Проверяем наличие структуры в StructureType
            try:
                StructureType(structure)
                return structure
            except ValueError:
                # Если точного совпадения нет, пробуем найти ближайшее
                structure_mapping = {
                    'three': 'three_act',
                    'three-act': 'three_act',
                    'three act': 'three_act',
                    'four': 'four_act',
                    'four-act': 'four_act',
                    'four act': 'four_act',
                    'hero': 'vogler_hero_journey',
                    "hero's journey": 'vogler_hero_journey',
                    'heros journey': 'vogler_hero_journey',
                    'eight point': 'watts_eight_point_arc',
                    'eight-point': 'watts_eight_point_arc',
                    'watts': 'watts_eight_point_arc',
                    'field': 'field_paradigm',
                    'paradigm': 'field_paradigm',
                    'campbell': 'monomyth',
                    'soth': 'soth_story_structure',
                    'mini-movie': 'soth_story_structure',
                    'mini movie': 'soth_story_structure',
                    'harmon': 'harmon_story_circle',
                    'story circle': 'harmon_story_circle',
                    'gulino': 'gulino_sequence',
                    'sequence': 'gulino_sequence'
                }
                
                # Ищем ближайшее совпадение
                for key, value in structure_mapping.items():
                    if key in structure:
                        return value
                
                logger.warning(f"Could not map structure '{structure}' to known type")
                return "three_act"  # Возвращаем three_act как наиболее общую структуру
                
        except Exception as e:
            logger.error(f"Error in classify: {e}")
            return "three_act"  # В случае ошибки возвращаем three_act как безопасный вариант


    def evaluate(self, text: str, structure_name: str = None) -> dict:
        """
        Проводит полный анализ текста согласно определенной структуре.
        """
        if structure_name is None:
            structure_name = self.classify(text)

        # Извлекаем базовую структуру
        structure = extract_structure(text)
        
        # Конвертируем в нужный формат
        formatted_structure = convert_to_format(structure, structure_name)
        
        # Получаем класс для работы с выбранной структурой
        StructureClass = get_narrative_structure(structure_name)  # Get the class
        narrative_structure = StructureClass()  # Create the instance
        
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
        """
        try:
            # Формируем промпт для анализа
            display_name = StructureType.get_display_name(structure)
            prompt = f"""Analyze the following text according to the {display_name} narrative structure. 
            NEVER try to guess what this script is film from! 
            Provide a detailed breakdown of how the text fits or doesn't fit this structure:

            {text}"""
            
            response = self._call_llm(prompt)
            
            try:
                structure_type = StructureType(structure)
            except ValueError:
                logger.warning(f"Structure not found: {structure}. Using default structure.")
                structure_type = StructureType.THREE_ACT
                structure = structure_type.value

            # Получаем класс структуры и создаем экземпляр
            StructureClass = get_narrative_structure(structure_type)  # Get the class
            narrative_structure = StructureClass()  # Create the instance
            
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
            
            # Убедимся, что response - строка
            if not isinstance(response, str):
                response = str(response)
            
            return {
                "structure": display_name,
                "analysis": response,
                "formatted_structure": formatted_structure,
                "structure_analysis": structure_analysis,
                "visualization": visualization
            }
        except Exception as e:
            logger.error(f"Error in analyze_specific_structure: {e}")
            raise


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
