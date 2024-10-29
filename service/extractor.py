# service/extractor.py

import spacy
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

# Загружаем модель один раз при импорте модуля
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.error("Failed to load en_core_web_sm. Please install it with: python -m spacy download en_core_web_sm")
    raise

def extract_structure(text: str) -> Dict[str, Any]:
    """
    Извлекает базовую структуру из текста, включая предложения, сущности и метрики.
    
    Args:
        text: Входной текст для анализа
        
    Returns:
        Dict[str, Any]: Словарь с извлеченной структурой, содержащий:
            - sentences: список предложений
            - entities: список именованных сущностей
            - word_count: количество слов
            - sentence_count: количество предложений
            - avg_sentence_length: средняя длина предложения
            - paragraphs: список параграфов
            - discourse_markers: маркеры связности текста
    """
    try:
        # Обработка текста
        doc = nlp(text)
        
        # Извлечение предложений
        sentences = [sent.text.strip() for sent in doc.sents]
        
        # Извлечение сущностей с их типами
        entities = [{
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        } for ent in doc.ents]
        
        # Разделение на параграфы
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Поиск дискурсивных маркеров
        discourse_markers = [
            token.text for token in doc 
            if token.dep_ in ['mark', 'cc'] or 
            token.text.lower() in ['however', 'therefore', 'thus', 'moreover']
        ]
        
        # Подсчет метрик
        word_count = len([token for token in doc if not token.is_punct])
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        structure = {
            "sentences": sentences,
            "entities": entities,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 2),
            "paragraphs": paragraphs,
            "discourse_markers": discourse_markers,
            "metadata": {
                "language": doc.lang_,
                "has_entities": bool(entities),
                "complexity_score": calculate_complexity_score(doc)
            }
        }
        
        return structure
        
    except Exception as e:
        logger.error(f"Error extracting structure: {str(e)}")
        # Возвращаем базовую структуру в случае ошибки
        return {
            "sentences": [text],
            "entities": [],
            "word_count": len(text.split()),
            "sentence_count": 1,
            "error": str(e)
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
