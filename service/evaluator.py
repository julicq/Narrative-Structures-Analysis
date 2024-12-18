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

class NarrativeEvaluator:
    """
    Класс для оценки и анализа нарративных структур текста.
    """
    
    def __init__(self, llm: Any, gigachat_token: Optional[str] = None, model_type: str = "ollama"):
        """
        Инициализация оценщика нарративных структур.
        
        Args:
            llm: Основная модель (Ollama)
            gigachat_token: Токен для GigaChat (опционально)
            model_type: Тип модели (по умолчанию "ollama")
        """
        self.llm = llm
        self.structure_converter = StoryStructureConverter()
        self.gigachat: Optional[GigaChat] = None
        self.gigachat_token = gigachat_token
        self.model_type = model_type
        
        # Инициализация промптов
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
        """Инициализация промптов на разных языках."""
        # Английские промпты
        self.prompts_en: Dict[str, str] = {
            "classify": """As a screenplay structure expert, analyze this screenplay and determine its narrative structure. 
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

            Structure identifier:""",
            
            "analyze": """Analyze the following text according to the {structure_name} narrative structure.
            NEVER try to guess what this script is film from!
            Provide a detailed breakdown of how the text fits or doesn't fit this structure.
            Focus on:
            1. Key structural elements
            2. Character development
            3. Plot progression
            4. Dramatic tension
            5. Theme development

            Text to analyze:
            {text}"""
        }
        
        # Русские промпты
        self.prompts_ru: Dict[str, str] = {
            "classify": """Как эксперт по структуре сценариев, проанализируйте этот сценарий и определите его нарративную структуру.
            Учитывайте следующие аспекты:
            1. Развитие сюжета и основные поворотные моменты
            2. Арки развития персонажей
            3. Структура актов и организация сцен
            4. Ключевые драматические моменты и их размещение
            
            Выберите НАИБОЛЕЕ ПОДХОДЯЩУЮ структуру из этих вариантов:
            1. "watts_eight_point_arc" - Восьмиточечная арка (Найджел Уоттс)
            - Стазис → Триггер → Поиск → Сюрприз → Критический выбор → Кульминация → Разворот → Развязка
            
            2. "vogler_hero_journey" - Путешествие героя (Кристофер Воглер)
            - Обычный мир → Зов к приключениям → Отказ → Встреча с наставником → Пересечение порога → Испытания, союзники, враги → Приближение → Кризис → Награда → Обратный путь → Воскрешение → Возвращение
            
            3. "three_act" - Трёхактная структура
            - Завязка (Акт 1) → Конфронтация (Акт 2) → Развязка (Акт 3)
            - С чётким инцидентом-завязкой, средней точкой и кульминацией
            
            4. "four_act" - Четырёхактная структура
            - Завязка → Развитие → Кульминация → Развязка
            - Каждый акт примерно 25-30 страниц
            
            5. "field_paradigm" - Парадигма (Сид Филд)
            - Завязка → Поворотный пункт 1 → Конфронтация → Поворотный пункт 2 → Развязка
            - Особый акцент на поворотных пунктах
            
            6. "monomyth" - Мономиф (Джозеф Кэмпбелл)
            - Уход → Инициация → Возвращение
            - Фокус на психологическом/мифологическом путешествии героя
            
            7. "soth_story_structure" - Метод мини-фильма (Крис Сот)
            - Восемь чётких 15-минутных сегментов
            - Каждый сегмент со своей драматической аркой
            
            8. "harmon_story_circle" - Сюжетный круг (Дэн Хармон)
            - Ты → Потребность → Уход → Поиск → Находка → Получение → Возвращение → Изменение
            
            9. "gulino_sequence" - Последовательный подход (Пол Гулино)
            - Восемь 8-15-страничных последовательностей
            - Каждая последовательность как мини-фильм

            Проанализируйте следующий отрывок сценария и верните ТОЛЬКО идентификатор структуры (например, "three_act"), 
            которая лучше всего подходит. Если определить невозможно, верните "unknown".

            Сценарий:
            {text}

            Идентификатор структуры:""",
            
            "analyze": """Проанализируйте следующий текст в соответствии со структурой {structure_name}.
            НИКОГДА не пытайтесь угадать, из какого это фильма!
            Предоставьте подробный разбор того, как текст соответствует или не соответствует этой структуре.
            Сосредоточьтесь на:
            1. Ключевых структурных элементах
            2. Развитии персонажей
            3. Развитии сюжета
            4. Драматическом напряжении
            5. Развитии темы

            Текст для анализа:
            {text}"""
        }

    def _detect_language(self, text: str) -> str:
        """
        Определяет язык текста.
        
        Args:
            text: Текст для анализа
            
        Returns:
            str: Код языка ('ru' или 'en')
        """
        try:
            lang = langdetect.detect(text)
            return 'ru' if lang == 'ru' else 'en'
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return 'en'

    def _get_prompt(self, prompt_key: str, text: str, **kwargs) -> str:
        """
        Возвращает промпт на соответствующем языке.
        
        Args:
            prompt_key: Ключ промпта
            text: Анализируемый текст
            **kwargs: Дополнительные параметры для форматирования
        """
        lang = self._detect_language(text)
        # Используем русские промпты для русского текста
        if lang == 'ru':
            # Если есть GigaChat - используем его
            if self.gigachat:
                prompts = self.prompts_ru
            # Если GigaChat нет, но текст русский - все равно используем русские промпты
            else:
                prompts = self.prompts_ru
                logger.warning("Russian text detected but GigaChat is not available. Using Russian prompts with main LLM.")
        else:
            prompts = self.prompts_en
        
        try:
            return prompts[prompt_key].format(text=text, **kwargs)
        except KeyError:
            logger.error(f"Prompt key '{prompt_key}' not found in {lang} prompts")
            raise
        except Exception as e:
            logger.error(f"Error formatting prompt: {e}")
            raise

    def _call_llm(self, prompt: str) -> str:
        """
        Вызывает LLM с учетом языка промпта.
        
        Args:
            prompt: Текст промпта
            
        Returns:
            str: Ответ модели
        """
        lang = self._detect_language(prompt)
        
        try:
            # Для русского текста пробуем сначала GigaChat
            if lang == 'ru' and self.gigachat:
                try:
                    # Проверяем длину промпта
                    max_length = 30_000  # Оставляем запас от лимита в 32К
                    if len(prompt) > max_length:
                        prompt = prompt[:max_length] + "\n...\nПожалуйста, проанализируйте доступную часть текста."
                    # Форматируем промпт для GigaChat
                    formatted_prompt = self._format_prompt_for_gigachat(prompt)
                    messages = [
                        {
                            "role": "system",
                            "content": (
                                "Вы - эксперт по анализу сценариев и нарративных структур. "
                                "Ваша задача - анализировать тексты и определять их структурные элементы. "
                                "Отвечайте структурированно, используя профессиональную терминологию."
                            )
                        },
                        {
                            "role": "user",
                            "content": formatted_prompt
                        }
                    ]
                    response = self.gigachat.chat(messages)
                    return response.choices[0].message.content
                except Exception as e:
                    logger.warning(f"GigaChat failed: {e}")
                    # Если произошла ошибка с GigaChat, переходим к основной модели
            
            # Добавляем указание отвечать на русском для русскоязычных текстов
            if lang == 'ru':
                prompt = (
                    "Ты - эксперт по анализу сценариев. "
                    "ВАЖНО: Весь анализ должен быть предоставлен на русском языке. "
                    "Не обращай внимания на отдельные английские слова в сценарии. "
                    "Не используй английский язык в ответе.\n\n"
                    f"{prompt}"
                )

            # Используем основную модель
            response = self.llm.invoke(prompt)
            if hasattr(response, 'content'):
                return response.content
            return str(response)
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

    def _format_prompt_for_gigachat(self, prompt: str) -> str:
        """
        Форматирует промпт для GigaChat, убирая потенциально проблемные элементы форматирования.
        
        Args:
            prompt: Исходный промпт
            
        Returns:
            str: Отформатированный промпт
        """
        # Убираем специальные символы и форматирование
        formatted_prompt = prompt.replace('*', '')
        formatted_prompt = formatted_prompt.replace('_', '')
        formatted_prompt = formatted_prompt.replace('#', '')
        
        # Добавляем четкие разделители для структурных элементов
        formatted_prompt = formatted_prompt.replace(
            "Структурные элементы:",
            "\nСТРУКТУРНЫЕ ЭЛЕМЕНТЫ:\n"
        )
        
        # Форматируем акты и сцены
        lines = formatted_prompt.split('\n')
        formatted_lines = []
        for line in lines:
            if "Акт" in line or "Сцена" in line:
                formatted_lines.append(f"\n{line}")
            else:
                formatted_lines.append(line)
        
        return "\n".join(formatted_lines)

    def classify(self, text: str) -> str:
        """
        Классифицирует текст по типу нарративной структуры."""
        
        try:
            prompt = self._get_prompt("classify", text)
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
        Проводит полный анализ текста согласно определенной структуре с использованием RAG.
        
        Args:
            text: Входной текст для анализа
            structure_name: Название структуры (опционально)
            
        Returns:
            dict: Результаты анализа
        """
        try:
            # Определяем язык текста в начале метода
            lang = self._detect_language(text)
            logger.info(f"Detected language: {lang}")
            
            # Проверяем входные данные
            if not isinstance(text, str):
                logger.error(f"Invalid input type for text: {type(text)}")
                raise ValueError(f"Expected string, got {type(text)}")
            
            # Используем RAG для получения релевантных частей текста
            rag_context = self.rag_processor.process_text(text)
            if not rag_context.get("chunks"):
                raise ValueError("No chunks generated from RAG processor")

            # Получаем структуру для анализа
            narrative_structure = self.structure_converter.get_structure(structure_name)
            if not narrative_structure:
                error_message = "Ошибка: неверный тип структуры" if lang == 'ru' else "Error: invalid structure type"
                return {
                    "structure_name": "Error",
                    "llm_evaluation": error_message,
                    "structure_analysis": {},
                    "visualization": None,
                    "tokens_used": 0,
                    "error": "Invalid structure type"
                }

            # Если структура не указана, определяем её
            if structure_name is None:
                # Используем RAG для классификации на основе релевантных частей
                structure_name = self.classify(rag_context["chunks"][0])  # Используем первый чанк для определения структуры
            
            # Преобразуем строку в StructureType
            try:
                # Важно: преобразуем строку в enum
                structure_type = StructureType(structure_name.lower())  # добавляем .lower() для надежности
            except ValueError as e:
                logger.warning(f"Invalid structure_name: {structure_name}, falling back to THREE_ACT")
                structure_type = StructureType.THREE_ACT
            
            # Получаем класс структуры один раз
            narrative_structure = self.structure_converter.get_structure(structure_name)
            if not narrative_structure:
                error_message = "Ошибка: неверный тип структуры" if lang == 'ru' else "Error: invalid structure type"
                return {
                    "structure_name": "Error",
                    "llm_evaluation": error_message,
                    "structure_analysis": {},
                    "visualization": None,
                    "tokens_used": 0,
                    "error": "Invalid structure type"
                }
            
            # Извлекаем базовую структуру из обработанных RAG чанков
            combined_analysis = []
            for chunk in rag_context["chunks"]:
                # Извлекаем структуру из каждого чанка
                chunk_structure = extract_structure(chunk)
                combined_analysis.append(chunk_structure)
            
            # Объединяем результаты анализа чанков
            structure = self._merge_chunk_analyses(combined_analysis)
            
            # Конвертируем в нужный формат
            formatted_structure = convert_to_format(structure, structure_name)
            
            # Формирование промпта
            try:
                base_prompt = (
                    narrative_structure.get_prompt() if hasattr(narrative_structure, 'get_prompt')
                    else (
                        "Проанализируйте следующий текст, используя структуру {structure_name}:\n\n"
                        "{text}\n\n"
                        "Предоставьте подробный анализ."
                    ) if lang == 'ru' else (
                        "Analyze the following text using {structure_name} structure:\n\n"
                        "{text}\n\n"
                        "Provide detailed analysis."
                    )
                )

                # Сначала создаем enhanced_prompt с RAG
                enhanced_prompt = self._enhance_prompt_with_rag(
                    base_prompt, 
                    rag_context["chunks"], 
                    formatted_structure
                )

                # Затем добавляем инструкции для русского языка если нужно
                if lang == 'ru':
                    enhanced_prompt = (
                        "ИНСТРУКЦИЯ: Проведите анализ текста на русском языке, "
                        "используя профессиональную терминологию. "
                        "Структурируйте ответ по следующим разделам:\n"
                        "1. Общая структура\n"
                        "2. Анализ актов\n"
                        "3. Ключевые сюжетные точки\n"
                        "4. Развитие персонажей\n"
                        "5. Рекомендации по улучшению\n\n"
                        f"{enhanced_prompt}"
                    )

                llm_evaluation = self._call_llm(enhanced_prompt)

            except Exception as e:
                logger.error(f"Error during prompt evaluation: {e}")
                llm_evaluation = "Ошибка при анализе" if lang == 'ru' else "Error during evaluation"
            
            # Проводим структурный анализ
            try:
                structure_analysis = narrative_structure.analyze(formatted_structure)
                visualization = narrative_structure.visualize(structure_analysis)
            except Exception as e:
                logger.error(f"Error during structure analysis: {e}")
                structure_analysis = {}
                visualization = None
            
            tokens_used = self._estimate_tokens_used(text)

            return {
                "structure_name": narrative_structure.display_name,
                "llm_evaluation": llm_evaluation,
                "structure_analysis": structure_analysis,
                "visualization": visualization,
                "formatted_structure": formatted_structure,
                "raw_structure": structure,
                "tokens_used": tokens_used,
                "rag_context": {
                    "total_chunks": len(rag_context["chunks"]),
                    "processed_chunks": len(combined_analysis)
                }
            }
        
        except Exception as e:
            logger.error(f"Error during structure analysis: {e}")
            # Возвращаем базовый результат с минимальным количеством токенов
            return {
                "structure_name": "Error",
                "llm_evaluation": "Произошла ошибка при анализе",
                "structure_analysis": {},
                "visualization": None,
                "tokens_used": max(100, len(text.split()) * 2),  # Минимальное количество токенов
                "error": str(e)
            }

    def _estimate_tokens_used(self, text: str) -> int:
        """
        Оценивает количество использованных токенов.
        
        Args:
            text: Анализируемый текст
            
        Returns:
            int: Оценка количества токенов
        """
        # Простая оценка: примерно 4 токена на слово
        return len(text.split()) * 4

    def _merge_chunk_analyses(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Объединяет анализы отдельных чанков в единый анализ.
        
        Args:
            analyses: Список анализов чанков
            
        Returns:
            Dict[str, Any]: Объединенный анализ
        """
        if not analyses:
            return {}
        
        merged = {
            "acts": {},
            "elements": {},
            "themes": [],
            "character_arcs": {},
            "plot_points": []
        }
        
        for analysis in analyses:
            # Объединяем акты
            for act_name, act_data in analysis.get("acts", {}).items():
                if act_name not in merged["acts"]:
                    merged["acts"][act_name] = []
                merged["acts"][act_name].extend(act_data)
            
            # Объединяем элементы
            for elem_name, elem_data in analysis.get("elements", {}).items():
                if elem_name not in merged["elements"]:
                    merged["elements"][elem_name] = []
                merged["elements"][elem_name].extend(elem_data)
            
            # Объединяем темы
            merged["themes"].extend(analysis.get("themes", []))
            
            # Объединяем арки персонажей
            for char, arc in analysis.get("character_arcs", {}).items():
                if char not in merged["character_arcs"]:
                    merged["character_arcs"][char] = []
                merged["character_arcs"][char].extend(arc)
            
            # Объединяем ключевые точки сюжета
            merged["plot_points"].extend(analysis.get("plot_points", []))
        
        # Удаляем дубликаты
        merged["themes"] = list(set(merged["themes"]))
        merged["plot_points"] = list(set(merged["plot_points"]))
        
        return merged

    def _enhance_prompt_with_rag(
        self, 
        base_prompt: str, 
        rag_chunks: List[str], 
        formatted_structure: Dict[str, Any]
    ) -> str:
        """
        Улучшает базовый промпт контекстом из RAG.
        """
        # Ограничиваем длину контекста
        max_context_length = 4000  # Примерное ограничение для контекста
        
        # Форматируем контекст из чанков
        context_prompt = "\nРЕЛЕВАНТНЫЕ ФРАГМЕНТЫ ТЕКСТА:\n"
        total_length = len(context_prompt)
        
        # Берем только 2 наиболее релевантных чанка вместо 3
        for i, chunk in enumerate(rag_chunks[:2], 1):
            # Ограничиваем размер каждого чанка
            chunk_summary = chunk[:1000] + "..." if len(chunk) > 1000 else chunk
            chunk_text = f"\nФрагмент {i}:\n{chunk_summary}\n"
            
            if total_length + len(chunk_text) > max_context_length:
                break
                
            context_prompt += chunk_text
            total_length += len(chunk_text)
        
        # Ограничиваем информацию о структуре
        structure_prompt = "\nКЛЮЧЕВЫЕ СТРУКТУРНЫЕ ЭЛЕМЕНТЫ:\n"
        for key, value in formatted_structure.items():
            if isinstance(value, (list, dict)):
                # Ограничиваем количество элементов в списках
                if isinstance(value, list):
                    value = value[:3]  # Берем только первые 3 элемента
                elif isinstance(value, dict):
                    value = dict(list(value.items())[:3])  # Берем только первые 3 пары
            
            structure_info = f"\n{key}: {str(value)[:200]}...\n" if len(str(value)) > 200 else f"\n{key}: {value}\n"
            if total_length + len(structure_info) > max_context_length:
                break
                
            structure_prompt += structure_info
            total_length += len(structure_info)
        
        # Собираем финальный промпт с учетом ограничений
        final_prompt = (
            f"{base_prompt[:1000]}\n"  # Ограничиваем базовый промпт
            f"{context_prompt}\n"
            f"{structure_prompt}\n"
            "\nПожалуйста, предоставьте краткий анализ ключевых элементов."
        )
        
        return final_prompt