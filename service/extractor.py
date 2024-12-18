# service/extractor.py

import spacy
from typing import Dict, List, Any, Optional
import logging
from spacy.tokens import Doc
from spacy.language import Language

logger = logging.getLogger(__name__)

# Загружаем модели для разных языков
try:
    nlp_en = spacy.load("en_core_web_sm")
    nlp_ru = spacy.load("ru_core_news_sm")
except OSError as e:
    logger.error(f"Failed to load spaCy models: {e}")
    logger.error("Please install required models with:")
    logger.error("python -m spacy download en_core_web_sm")
    logger.error("python -m spacy download ru_core_news_sm")
    raise

def get_nlp_model(text: str) -> Language:
    """
    Определяет язык текста и возвращает соответствующую модель spaCy.
    
    Args:
        text: Входной текст
        
    Returns:
        Language: Модель spaCy для соответствующего языка
    """
    # Проверка входных данных
    if isinstance(text, dict):
        if "text" in text:
            text = text["text"]
        elif "content" in text:
            text = text["content"]
        else:
            logger.error("Could not extract text from dictionary")
            text = ""
    
    if not isinstance(text, str):
        logger.error(f"Unexpected input type in get_nlp_model: {type(text)}")
        text = str(text) if text is not None else ""

    # Простая эвристика для определения языка
    ru_chars = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    text_chars = set(text.lower())
    is_russian = len(text_chars & ru_chars) > 0
    
    return nlp_ru if is_russian else nlp_en

def extract_structure(text: str, chunk_size: Optional[int] = None) -> Dict[str, Any]:
    """
    Извлекает базовую структуру из текста с поддержкой чанкинга для RAG.
    Args:
        text: Входной текст для анализа
        chunk_size: Размер чанка (если None, обрабатывает весь текст целиком)
        
    Returns:
        Dict[str, Any]: Словарь с извлеченной структурой
    """
    try:
        # Проверяем тип входных данных
        if isinstance(text, dict):
            logger.warning("Received dict instead of string, attempting to extract text content")
            # Пытаемся извлечь текст из словаря
            if "text" in text:
                text = text["text"]
            elif "content" in text:
                text = text["content"]
            else:
                # Если не можем найти текст, возвращаем пустую структуру
                logger.error("Could not extract text from dictionary")
                return create_fallback_structure("")
        
        if not isinstance(text, str):
            logger.error(f"Unexpected input type: {type(text)}")
            return create_fallback_structure("")

        nlp = get_nlp_model(text)
        
        # Если указан размер чанка, разбиваем текст
        if chunk_size:
            structures = []
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i + chunk_size]
                chunk_structure = process_text_chunk(chunk, nlp)
                structures.append(chunk_structure)
            return merge_structures(structures)
        else:
            return process_text_chunk(text, nlp)
    except Exception as e:
        logger.error(f"Error extracting structure: {str(e)}")
        return create_fallback_structure("")  # Передаем пустую строку вместо словаря

def create_fallback_structure(text: str) -> Dict[str, Any]:
    """Создает базовую структуру в случае ошибки."""
    # Проверяем входные данные
    if not isinstance(text, str):
        text = str(text) if text is not None else ""
        
    return {
        "sentences": [text] if text else [],
        "entities": [],
        "word_count": len(text.split()) if text else 0,
        "sentence_count": 1 if text else 0,
        "paragraphs": [text] if text else [],
        "discourse_markers": [],
        "key_phrases": [],
        "semantic_roles": [],
        "metadata": {
            "language": "unknown",
            "complexity_score": 0.0,
            "error": "Processing failed"
        }
    }

def process_text_chunk(text: str, nlp: Language) -> Dict[str, Any]:
    """
    Обрабатывает отдельный чанк текста.
    
    Args:
        text: Текст для обработки
        nlp: Модель spaCy
        
    Returns:
        Dict[str, Any]: Структура чанка
    """
    doc = nlp(text)
    
    # Базовая структура
    structure = {
        "sentences": [sent.text.strip() for sent in doc.sents],
        "entities": extract_entities(doc),
        "word_count": len([token for token in doc if not token.is_punct]),
        "sentence_count": len(list(doc.sents)),
        "paragraphs": [p.strip() for p in text.split('\n\n') if p.strip()],
        "discourse_markers": extract_discourse_markers(doc),
        "key_phrases": extract_key_phrases(doc),
        "semantic_roles": extract_semantic_roles(doc),
        "metadata": create_metadata(doc)
    }
    
    # Добавляем метрики
    structure.update(calculate_metrics(doc))
    
    return structure

def merge_structures(structures: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Объединяет структуры из разных чанков.
    
    Args:
        structures: Список структур для объединения
        
    Returns:
        Dict[str, Any]: Объединенная структура
    """
    if not structures:
        return {}

    merged = {
        "sentences": [],
        "entities": [],
        "paragraphs": [],
        "discourse_markers": [],
        "key_phrases": [],
        "semantic_roles": [],
        "word_count": 0,
        "sentence_count": 0
    }
    
    # Объединяем все поля
    for struct in structures:
        merged["sentences"].extend(struct["sentences"])
        merged["entities"].extend(struct["entities"])
        merged["paragraphs"].extend(struct["paragraphs"])
        merged["discourse_markers"].extend(struct["discourse_markers"])
        merged["key_phrases"].extend(struct.get("key_phrases", []))
        merged["semantic_roles"].extend(struct.get("semantic_roles", []))
        merged["word_count"] += struct["word_count"]
        merged["sentence_count"] += struct["sentence_count"]
    
    # Вычисляем общие метрики
    if merged["sentence_count"] > 0:
        merged["avg_sentence_length"] = round(merged["word_count"] / merged["sentence_count"], 2)
    
    # Обновляем метаданные
    merged["metadata"] = {
        "total_chunks": len(structures),
        "language": structures[0]["metadata"]["language"],
        "complexity_score": sum(s["metadata"]["complexity_score"] for s in structures) / len(structures)
    }
    
    return merged

def extract_entities(doc: Doc) -> List[Dict[str, Any]]:
    """Извлекает именованные сущности с дополнительной информацией."""
    return [{
        "text": ent.text,
        "label": ent.label_,
        "start": ent.start_char,
        "end": ent.end_char,
        "description": spacy.explain(ent.label_)
    } for ent in doc.ents]

def extract_discourse_markers(doc: Doc) -> List[Dict[str, str]]:
    """Извлекает маркеры связности с их функциями."""
    markers = {
        "however": "contrast",
        "therefore": "conclusion",
        "thus": "conclusion",
        "moreover": "addition",
        "furthermore": "addition",
        "nevertheless": "contrast",
        "consequently": "conclusion",
        "meanwhile": "temporal",
        "afterward": "temporal",
        "finally": "sequence"
    }
    
    return [{
        "text": token.text,
        "function": markers.get(token.text.lower(), "connection")
    } for token in doc if token.text.lower() in markers or token.dep_ in ['mark', 'cc']]

def extract_key_phrases(doc: Doc) -> List[str]:
    """Извлекает ключевые фразы из текста."""
    try:
        # Проверяем поддержку noun_chunks для данного языка
        if doc.has_annotation("DEP") and doc.lang_ != 'ru':
            return [chunk.text for chunk in doc.noun_chunks]
        else:
            # Альтернативный метод для русского языка
            # Извлекаем существительные с прилагательными
            phrases = []
            for token in doc:
                if token.pos_ == "NOUN":
                    # Собираем прилагательные перед существительным
                    modifiers = []
                    for left_token in token.lefts:
                        if left_token.pos_ == "ADJ":
                            modifiers.append(left_token.text)
                    if modifiers:
                        phrases.append(" ".join(modifiers + [token.text]))
                    else:
                        phrases.append(token.text)
            return phrases
    except Exception as e:
        logger.warning(f"Error extracting key phrases: {e}")
        return []  # Возвращаем пустой список в случае ошибки

def extract_semantic_roles(doc: Doc) -> List[Dict[str, str]]:
    """Извлекает семантические роли из предложений."""
    roles = []
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ['nsubj', 'dobj', 'iobj']:
                roles.append({
                    "text": token.text,
                    "role": token.dep_,
                    "verb": token.head.text
                })
    return roles

def create_metadata(doc: Doc) -> Dict[str, Any]:
    """Создает расширенные метаданные для документа."""
    return {
        "language": doc.lang_,
        "complexity_score": calculate_complexity_score(doc),
        "has_entities": bool(doc.ents),
        "sentiment": analyze_sentiment(doc),
        "document_type": detect_document_type(doc)
    }

def calculate_metrics(doc: Doc) -> Dict[str, float]:
    """Вычисляет различные метрики текста."""
    sentences = list(doc.sents)
    if not sentences:
        return {"readability_score": 0.0, "coherence_score": 0.0}
    
    # Базовые метрики
    avg_words = sum(len([t for t in sent if not t.is_punct]) for sent in sentences) / len(sentences)
    
    return {
        "readability_score": calculate_readability(doc),
        "coherence_score": calculate_coherence(doc),
        "avg_words_per_sentence": round(avg_words, 2)
    }

def create_fallback_structure(text: str) -> Dict[str, Any]:
    """Создает базовую структуру в случае ошибки."""
    return {
        "sentences": [text],
        "entities": [],
        "word_count": len(text.split()),
        "sentence_count": 1,
        "paragraphs": [text],
        "discourse_markers": [],
        "key_phrases": [],
        "semantic_roles": [],
        "metadata": {
            "language": "unknown",
            "complexity_score": 0.0,
            "error": "Processing failed"
        }
    }

def calculate_complexity_score(doc) -> float:
    """
    Вычисляет оценку сложности текста на основе различных метрик.
    
    Args:
        doc: Обработанный spaCy документ
        
    Returns:
        float: Оценка сложности от 0 до 1
    """
    try:
        # Подсчет среднего количества слов в предложении
        sentences = list(doc.sents)
        if not sentences:
            return 0.0
            
        avg_words_per_sent = sum(len([token for token in sent if not token.is_punct]) 
                                for sent in sentences) / len(sentences)
        
        # Подсчет процента сложных слов (более 2 слогов)
        complex_words = len([token for token in doc 
                           if len([char for char in token.text.lower() 
                                 if char in 'aeiou']) > 2])
        complex_ratio = complex_words / len(doc) if len(doc) > 0 else 0
        
        # Нормализация и комбинирование метрик
        sent_complexity = min(avg_words_per_sent / 30.0, 1.0)  # нормализация до 1
        word_complexity = complex_ratio
        
        # Итоговая оценка (среднее значение)
        return round((sent_complexity + word_complexity) / 2.0, 3)
        
    except Exception as e:
        logger.warning(f"Error calculating complexity score: {str(e)}")
        return 0.0

def analyze_sentiment(doc: Doc) -> Dict[str, float]:
    """
    Анализирует эмоциональную окраску текста.
    
    Args:
        doc: Обработанный spaCy документ
        
    Returns:
        Dict[str, float]: Словарь с оценками тональности
    """
    # Базовый анализ на основе лексикона
    positive_words = {'good', 'great', 'excellent', 'wonderful', 'best', 'happy',
                     'хороший', 'отличный', 'прекрасный', 'замечательный', 'лучший', 'счастливый'}
    negative_words = {'bad', 'terrible', 'awful', 'worst', 'poor', 'sad',
                     'плохой', 'ужасный', 'худший', 'бедный', 'грустный'}
    
    # Подсчет позитивных и негативных слов
    positive_count = sum(1 for token in doc if token.text.lower() in positive_words)
    negative_count = sum(1 for token in doc if token.text.lower() in negative_words)
    
    total_words = len([token for token in doc if not token.is_punct])
    if total_words == 0:
        return {"positive": 0.0, "negative": 0.0, "neutral": 1.0}
    
    # Вычисление оценок
    positive_score = positive_count / total_words
    negative_score = negative_count / total_words
    neutral_score = 1.0 - (positive_score + negative_score)
    
    return {
        "positive": round(positive_score, 3),
        "negative": round(negative_score, 3),
        "neutral": round(neutral_score, 3)
    }

def detect_document_type(doc: Doc) -> str:
    """
    Определяет тип документа на основе его характеристик.
    
    Args:
        doc: Обработанный spaCy документ
        
    Returns:
        str: Тип документа
    """
    # Характеристики для определения типа
    dialogue_markers = sum(1 for token in doc if token.text in {'"', '"', '"', '«', '»'})
    scene_markers = sum(1 for sent in doc.sents 
                       if any(marker in sent.text.lower() 
                             for marker in ['int.', 'ext.', 'fade in:', 'cut to:']))
    narrative_markers = sum(1 for token in doc 
                          if token.dep_ in ['mark', 'advcl'] 
                          or token.pos_ == 'VERB')
    
    # Определение типа на основе преобладающих характеристик
    if scene_markers > 0 and dialogue_markers / len(doc) > 0.1:
        return "screenplay"
    elif dialogue_markers / len(doc) > 0.2:
        return "dialogue"
    elif narrative_markers / len(doc) > 0.3:
        return "narrative"
    else:
        return "general"

def calculate_readability(doc: Doc) -> float:
    """
    Вычисляет оценку читабельности текста (упрощенная формула Флеша-Кинкейда).
    
    Args:
        doc: Обработанный spaCy документ
        
    Returns:
        float: Оценка читабельности от 0 до 1
    """
    try:
        sentences = list(doc.sents)
        if not sentences:
            return 0.0
        
        # Подсчет слов и предложений
        word_count = len([token for token in doc if not token.is_punct])
        sentence_count = len(sentences)
        
        # Подсчет слогов (упрощенный)
        syllable_count = sum(len([char for char in token.text.lower() if char in 'aeiouаеёиоуыэюя'])
                            for token in doc if not token.is_punct)
        
        if word_count == 0 or sentence_count == 0:
            return 0.0
        
        # Вычисление метрик
        words_per_sentence = word_count / sentence_count
        syllables_per_word = syllable_count / word_count
        
        # Нормализация оценки от 0 до 1
        score = 1.0 - ((0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59) / 100.0)
        return max(0.0, min(1.0, score))
        
    except Exception as e:
        logger.warning(f"Error calculating readability score: {str(e)}")
        return 0.0

def calculate_coherence(doc: Doc) -> float:
    """
    Вычисляет оценку связности текста.
    
    Args:
        doc: Обработанный spaCy документ
        
    Returns:
        float: Оценка связности от 0 до 1
    """
    try:
        # Подсчет связующих элементов
        discourse_markers = sum(1 for token in doc 
                              if token.dep_ in ['mark', 'cc'] 
                              or token.text.lower() in {
                                  'however', 'therefore', 'thus', 'moreover',
                                  'однако', 'поэтому', 'таким образом', 'кроме того'
                              })
        
        # Подсчет кореферентных связей (если доступно)
        corefs = 0
        if doc.has_annotation("DEP"):
            corefs = sum(1 for token in doc if token.dep_ in ['nsubj', 'dobj'] and token.head.i != token.i)
        
        # Подсчет тематических связей
        content_words = [token.text.lower() for token in doc 
                        if token.pos_ in {'NOUN', 'VERB', 'ADJ'} and not token.is_stop]
        
        if not content_words:
            return 0.0
        
        # Вычисление метрик
        sentences = list(doc.sents)
        sent_count = len(sentences)
        if sent_count <= 1:
            return 1.0
            
        # Нормализация метрик
        marker_score = min(discourse_markers / sent_count, 1.0)
        coref_score = min(corefs / sent_count, 1.0)
        
        # Итоговая оценка
        coherence_score = (marker_score + coref_score) / 2.0
        return round(coherence_score, 3)
        
    except Exception as e:
        logger.warning(f"Error calculating coherence score: {str(e)}")
        return 0.0

