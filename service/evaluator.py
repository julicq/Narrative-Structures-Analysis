# service/evaluator.py

import logging
from narr_mod import StructureType, get_narrative_structure
from service.rag_processor import NarrativeRAGProcessor
from .extractor import extract_structure
from .converter import convert_to_format, StoryStructureConverter
from typing import List, Dict, Any, Optional, Union
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import langdetect

logger = logging.getLogger(__name__)

class BaseStructureDefinition:
    """Базовый класс для определения структуры повествования"""
    def __init__(self):
        self.display_name = "Base Structure"
    
    def analyze(self, structure):
        raise NotImplementedError("Analyze method must be implemented")
    
    def visualize(self, analysis):
        raise NotImplementedError("Visualize method must be implemented")
    
    def get_prompt(self):
        raise NotImplementedError("Get prompt method must be implemented")

class NarrativeEvaluator:
    """Класс для оценки и анализа нарративных структур текста."""
    
    def __init__(self, llm: Any, gigachat_token: Optional[str] = None, model_type: str = "ollama"):
        self.llm = llm
        self.structure_converter = StoryStructureConverter()
        self.gigachat: Optional[GigaChat] = None
        self.gigachat_token = gigachat_token
        self.model_type = model_type
        self.max_tokens = 25000
        self.max_chunk_size = 2000
        self.max_entities = 3
        self.max_chunks = 3
        
        self._init_prompts()
        credentials = {"token": gigachat_token} if gigachat_token else None
        self.rag_processor = NarrativeRAGProcessor(llm, credentials)

        if gigachat_token:
            try:
                self.gigachat = GigaChat(credentials=gigachat_token)
                logger.info("GigaChat initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize GigaChat: {e}")

    def _init_prompts(self) -> None:
        """Инициализация сокращенных промптов для оптимизации токенов"""
        self.prompts_en = {
            "classify": """Analyze this screenplay and determine its structure type.
            Choose from: three_act, four_act, vogler_hero_journey, watts_eight_point_arc, 
            field_paradigm, monomyth, soth_story_structure, harmon_story_circle, gulino_sequence.
            Return ONLY the structure identifier.

            Text: {text}

            Structure:""",
            
            "analyze": """Analyze using {structure_name} structure.
            Focus on: key elements, character development, plot progression.
            Be concise.

            Text: {text}"""
        }
        
        self.prompts_ru = {
            "classify": """Определите структуру сценария.
            Варианты: three_act, four_act, vogler_hero_journey, watts_eight_point_arc,
            field_paradigm, monomyth, soth_story_structure, harmon_story_circle, gulino_sequence.
            Верните ТОЛЬКО идентификатор структуры.

            Текст: {text}

            Структура:""",
            
            "analyze": """Анализ по структуре {structure_name}.
            Фокус на: ключевых элементах, развитии персонажей, развитии сюжета.
            Будьте лаконичны.

            Текст: {text}"""
        }
    def _detect_language(self, text: str) -> str:
        """Определяет язык текста."""
        try:
            return 'ru' if langdetect.detect(text[:1000]) == 'ru' else 'en'
        except Exception:
            return 'en'

    def _get_prompt(self, prompt_key: str, text: str, **kwargs) -> str:
        """Возвращает оптимизированный промпт на соответствующем языке."""
        lang = self._detect_language(text)
        prompts = self.prompts_ru if lang == 'ru' else self.prompts_en
        
        try:
            return prompts[prompt_key].format(
                text=text[:self.max_chunk_size],
                **kwargs
            )
        except Exception as e:
            logger.error(f"Error formatting prompt: {e}")
            raise

    def _call_llm(self, prompt: str) -> str:
        """Вызывает LLM с оптимизированным промптом."""
        lang = self._detect_language(prompt)
        
        try:
            if lang == 'ru' and self.gigachat:
                try:
                    prompt = prompt[:self.max_chunk_size]
                    messages = [
                        {
                            "role": "system",
                            "content": "Вы - эксперт по анализу сценариев. Давайте краткие структурированные ответы."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                    response = self.gigachat.chat(messages)
                    return response.choices[0].message.content
                except Exception as e:
                    logger.warning(f"GigaChat failed: {e}")
            if lang == 'ru':
                prompt = f"Ответьте кратко на русском языке:\n{prompt}"
            response = self.llm.invoke(prompt)
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

    def classify(self, text: str) -> str:
        """Классифицирует текст по типу нарративной структуры."""
        try:
            prompt = self._get_prompt("classify", text)
            response = self._call_llm(prompt).strip().lower()
            
            try:
                return StructureType(response).value
            except ValueError:
                structure_mapping = {
                    'three': 'three_act',
                    'four': 'four_act',
                    'hero': 'vogler_hero_journey',
                    'eight': 'watts_eight_point_arc',
                    'field': 'field_paradigm',
                    'mono': 'monomyth',
                    'soth': 'soth_story_structure',
                    'harmon': 'harmon_story_circle',
                    'gulino': 'gulino_sequence'
                }
                
                for key, value in structure_mapping.items():
                    if key in response:
                        return value
                
                return "three_act"
                
        except Exception as e:
            logger.error(f"Error in classify: {e}")
            return "three_act"
    def evaluate(self, text: str, structure_name: str = None) -> dict:
        """Проводит оптимизированный анализ текста."""
        try:
            lang = self._detect_language(text)
            
            if not isinstance(text, str):
                raise ValueError(f"Expected string, got {type(text)}")
            
            # Получаем ограниченный контекст RAG
            rag_context = self.rag_processor.process_text(text)
            chunks = rag_context.get("chunks", [])[:self.max_chunks]
            
            if not chunks:
                raise ValueError("No chunks generated")

            # Определяем структуру
            if structure_name is None:
                structure_name = self.classify(chunks[0]["content"])
            
            try:
                structure_type = StructureType(structure_name.lower())
            except ValueError:
                structure_type = StructureType.THREE_ACT
                structure_name = "three_act"
            
            # Получаем и проверяем структуру
            narrative_structure = self.structure_converter.get_structure(structure_name)
            if not narrative_structure:
                raise ValueError("Invalid structure type")
            
            # Анализируем структуру
            combined_analysis = []
            for chunk in chunks:
                chunk_structure = extract_structure(chunk["content"])
                if chunk_structure:
                    combined_analysis.append(chunk_structure)
            
            # Форматируем структуру
            formatted_structure = convert_to_format(
                self._merge_chunk_analyses(combined_analysis),
                structure_name
            )
            
            # Получаем анализ LLM
            try:
                enhanced_prompt = self._enhance_prompt_with_rag(
                    self._get_prompt("analyze", text, structure_name=structure_name),
                    chunks,
                    formatted_structure
        )
                llm_evaluation = self._call_llm(enhanced_prompt)
            except Exception as e:
                logger.error(f"Error in LLM evaluation: {e}")
                llm_evaluation = "Ошибка анализа" if lang == 'ru' else "Analysis error"
        
            # Проводим структурный анализ
            try:
                if hasattr(narrative_structure, 'analyze'):
                    structure_analysis = narrative_structure.analyze(formatted_structure)
                else:
                    structure_analysis = {"raw_structure": formatted_structure}

                visualization = (
                    narrative_structure.visualize(structure_analysis)
                    if hasattr(narrative_structure, 'visualize')
                    else None
                )
            except Exception as e:
                logger.error(f"Error in structure analysis: {e}")
                structure_analysis = {"error": str(e)}
                visualization = None
            
            result = {
                "structure_name": getattr(narrative_structure, 'display_name', structure_name),
                "llm_evaluation": llm_evaluation,
                "structure_analysis": structure_analysis,
                "visualization": visualization,
                "formatted_structure": formatted_structure,
                "tokens_used": self._estimate_tokens_used(text),
                "rag_context": {
                    "total_chunks": len(chunks),
                    "processed_chunks": len(combined_analysis)
                }
            }
            
            return self._limit_result_size(result)
            
        except Exception as e:
            logger.error(f"Error in evaluate: {e}")
            return self._limit_result_size({
                "structure_name": "Error",
                "llm_evaluation": "Произошла ошибка при анализе" if lang == 'ru' else "Analysis failed",
                "structure_analysis": {},
                "visualization": None,
                "tokens_used": max(100, len(text.split()) * 2),
                "error": str(e)
            })

    def _merge_chunk_analyses(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Объединяет анализы чанков с ограничением размера."""
        if not analyses:
            return {}
        
        merged = {
            "acts": {},
            "elements": {},
            "themes": [],
            "character_arcs": {},
            "plot_points": []
        }
        
        for analysis in analyses[:self.max_chunks]:
            # Ограничиваем количество элементов в каждой категории
            for act_name, act_data in list(analysis.get("acts", {}).items())[:3]:
                if act_name not in merged["acts"]:
                    merged["acts"][act_name] = []
                merged["acts"][act_name].extend(act_data[:3])
            
            for elem_name, elem_data in list(analysis.get("elements", {}).items())[:3]:
                if elem_name not in merged["elements"]:
                    merged["elements"][elem_name] = []
                merged["elements"][elem_name].extend(elem_data[:3])
            
            merged["themes"].extend(analysis.get("themes", [])[:3])
            
            for char, arc in list(analysis.get("character_arcs", {}).items())[:3]:
                if char not in merged["character_arcs"]:
                    merged["character_arcs"][char] = []
                merged["character_arcs"][char].extend(arc[:3])
            
            merged["plot_points"].extend(analysis.get("plot_points", [])[:3])
        
        # Удаляем дубликаты и ограничиваем размер
        merged["themes"] = list(set(merged["themes"]))[:5]
        merged["plot_points"] = list(set(merged["plot_points"]))[:5]
        return merged

    def _enhance_prompt_with_rag(
        self,
        base_prompt: str,
        chunks: List[Dict[str, Any]],
        formatted_structure: Dict[str, Any]
    ) -> str:
        """Создает оптимизированный промпт с контекстом RAG."""
        context_prompt = "\nКлючевые фрагменты:\n"
        
        # Берем только один наиболее релевантный чанк
        if chunks:
            chunk = chunks[0]["content"]
            context_prompt += f"\n{chunk[:500]}...\n"
        
        # Ограничиваем структурную информацию
        structure_prompt = "\nКлючевые элементы:\n"
        essential_keys = ['acts', 'plot_points', 'character_arcs']
        
        for key in essential_keys:
            if key in formatted_structure:
                value = formatted_structure[key]
                if isinstance(value, (list, dict)):
                    if isinstance(value, list):
                        value = value[:2]
                    elif isinstance(value, dict):
                        value = dict(list(value.items())[:2])
                structure_prompt += f"{key}: {str(value)[:100]}...\n"
        
        return f"{base_prompt[:500]}\n{context_prompt}\n{structure_prompt}\nПроведите краткий анализ."

    def _limit_result_size(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Ограничивает размер результата для оптимизации токенов."""
        def truncate_text(text: str, max_length: int) -> str:
            return text[:max_length] + "..." if len(text) > max_length else text

        if "llm_evaluation" in result:
            result["llm_evaluation"] = truncate_text(result["llm_evaluation"], 3000)

        if "structure_analysis" in result and isinstance(result["structure_analysis"], dict):
            for key in result["structure_analysis"]:
                if isinstance(result["structure_analysis"][key], str):
                    result["structure_analysis"][key] = truncate_text(
                        result["structure_analysis"][key], 1000
                    )
                elif isinstance(result["structure_analysis"][key], list):
                    result["structure_analysis"][key] = result["structure_analysis"][key][:5]

        if "formatted_structure" in result:
            for key in result["formatted_structure"]:
                if isinstance(result["formatted_structure"][key], str):
                    result["formatted_structure"][key] = truncate_text(
                        result["formatted_structure"][key], 500
                    )
                elif isinstance(result["formatted_structure"][key], list):
                    result["formatted_structure"][key] = result["formatted_structure"][key][:3]

        return result

    def _estimate_tokens_used(self, text: str) -> int:
        """Оценивает количество использованных токенов."""
        # Приблизительная оценка: 1 слово ≈ 1.3 токена
