import pytest
import numpy as np
from service.multilingual_embeddings import MultilingualEmbeddings

@pytest.fixture
def embeddings():
    return MultilingualEmbeddings()

def calculate_cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def test_russian_embeddings(embeddings):
    russian_text = "Это тестовый текст на русском языке"
    russian_embedding = embeddings.embed_query(russian_text)
    assert len(russian_embedding) == 768, "Неверная размерность вектора для русского текста"

def test_english_embeddings(embeddings):
    english_text = "This is a test text in English"
    english_embedding = embeddings.embed_query(english_text)
    assert len(english_embedding) == 768, "Неверная размерность вектора для английского текста"

def test_cross_lingual_similarity(embeddings):
    text1 = "Кошка сидит на подоконнике"
    text2 = "The cat is sitting on the windowsill"
    
    emb1 = embeddings.embed_query(text1)
    emb2 = embeddings.embed_query(text2)
    
    similarity = calculate_cosine_similarity(emb1, emb2)
    assert similarity > 0.7, f"Низкая кросс-языковая схожесть: {similarity}"

def test_batch_embeddings(embeddings):
    texts = [
        "Первый текст на русском",
        "Second text in English",
        "Третий текст на русском",
        "Fourth text in English"
    ]
    
    batch_embeddings = embeddings.embed_documents(texts)
    assert len(batch_embeddings) == len(texts), "Неверное количество эмбеддингов в батче"
    assert all(len(emb) == 768 for emb in batch_embeddings), "Неверная размерность векторов в батче"

def test_embedding_consistency(embeddings):
    text = "Многоязычный текст with mixed languages"
    emb1 = embeddings.embed_query(text)
    emb2 = embeddings.embed_query(text)
    
    similarity = calculate_cosine_similarity(emb1, emb2)
    assert similarity > 0.99, "Эмбеддинги одного текста должны быть идентичны"

@pytest.mark.parametrize("text", [
    "",  # пустой текст
    "   ",  # только пробелы
    "a",  # один символ
    "." * 1000  # очень длинный текст
])
def test_edge_cases(embeddings, text):
    try:
        embedding = embeddings.embed_query(text)
        assert len(embedding) == 768, f"Неверная размерность вектора для текста: {text[:20]}..."
    except Exception as e:
        pytest.fail(f"Ошибка при обработке текста: {text[:20]}... | {str(e)}")