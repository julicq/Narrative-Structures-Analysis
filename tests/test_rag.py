import pytest
import warnings
import numpy as np
from service.rag_processor import NarrativeRAGProcessor
from service.llm import initialize_llm

# Настройка игнорирования предупреждений
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Специфичные предупреждения для torch
warnings.filterwarnings("ignore", message=".*torch.*")
warnings.filterwarnings("ignore", message=".*cuda.*")
warnings.filterwarnings("ignore", message=".*DataLoader.*")
@pytest.fixture(autouse=True)
def ignore_warnings():
    """Фикстура для игнорирования предупреждений во время тестов"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield

@pytest.fixture
def rag_processor():
    llm = initialize_llm()
    return NarrativeRAGProcessor(llm, credentials={})
        
def test_text_processing_basic(rag_processor):
    """Тест базовой обработки текста"""
    text = "Test narrative text for basic processing."
    result = rag_processor.process_text(text)
    
    assert "chunks" in result, "Отсутствует поле 'chunks' в результате"
    assert "vector_store_status" in result, "Отсутствует поле 'vector_store_status'"
    assert "document_structure" in result, "Отсутствует поле 'document_structure'"
    assert "document_metadata" in result, "Отсутствует поле 'document_metadata'"
    assert "document_type" in result["document_metadata"], "Отсутствует поле 'document_type' в метаданных"

def test_text_processing_multilingual(rag_processor):
    """Тест обработки многоязычного текста"""
    text = (
        "This is an English paragraph.\n"
        "Это параграф на русском языке."
    )
    result = rag_processor.process_text(text)
    
    assert result["document_metadata"]["language"] in ["en", "ru"]
    assert len(result["chunks"]) > 0

def test_structure_analysis(rag_processor):
    """Тест анализа структуры текста"""
    text = (
        "Chapter 1: Introduction\n"
        "This is a test narrative with some key elements. "
        "The story begins with a clear setup and continues "
        "through various plot points. Characters develop "
        "throughout the narrative arc."
    )
    result = rag_processor.process_text(text)
    assert "document_structure" in result
    
    analysis_result = rag_processor.analyze_structure(
        structure_type="narrative",
        prompt="Analyze the structure"
    )
    
    # Проверяем наличие всех ключевых полей
    assert isinstance(analysis_result, dict), "Result should be a dictionary"
    assert "analysis" in analysis_result, "Missing 'analysis' field"
    assert isinstance(analysis_result.get("confidence_score", 0.0), float), "Invalid confidence score"
    assert isinstance(analysis_result.get("structural_coverage", 0.0), float), "Invalid structural coverage"
    
    # Проверяем, что оценки находятся в допустимом диапазоне
    assert 0 <= analysis_result.get("confidence_score", 0.0) <= 1, "Confidence score out of range"
    assert 0 <= analysis_result.get("structural_coverage", 0.0) <= 1, "Structural coverage out of range"


def test_prompt_enhancement(rag_processor):
    """Тест улучшения промпта контекстом"""
    text = "Sample text for testing."
    rag_processor.process_text(text)
    
    base_prompt = "Analyze the text"
    enhanced_prompt = rag_processor._enhance_prompt_with_structure(
        base_prompt=base_prompt,
        structure_type="analysis"
    )
    
    assert len(enhanced_prompt) > len(base_prompt)
    assert "Document Analysis Context" in enhanced_prompt
    assert "Type:" in enhanced_prompt

@pytest.mark.parametrize("text", [
    "",  # пустой текст
    "   ",  # только пробелы
    "A" * 100,  # длинный текст
])
def test_edge_cases(rag_processor, text):
    """Тест граничных случаев"""
    try:
        result = rag_processor.process_text(text)
        assert isinstance(result, dict)
        assert "document_metadata" in result
        assert "document_type" in result["document_metadata"]
        assert result["document_metadata"]["document_type"] in ["unknown", "text"]
    except Exception as e:
        pytest.fail(f"Ошибка при обработке текста: {str(e)}")

@pytest.mark.skip_on_gpu  # Пропускаем тест на GPU
def test_vector_store_persistence(rag_processor):
    """Тест сохранения состояния векторного хранилища"""
    text = "Short test text."
    result = rag_processor.process_text(text)
    
    assert rag_processor.vector_store is not None
    # Проверяем базовую функциональность без intensive операций
    assert result["vector_store_status"] == "created"

def test_error_handling():
    """Тест обработки ошибок"""
    llm = initialize_llm()
    rag = NarrativeRAGProcessor(llm, credentials={})
    with pytest.raises(ValueError):
        # Должен вызвать ошибку, так как векторное хранилище не инициализировано
        rag.analyze_structure("narrative", "Analyze this")

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "skip_on_gpu: mark test to skip when running on GPU"
    )

@pytest.fixture(autouse=True)
def skip_on_gpu(request):
    if request.node.get_closest_marker('skip_on_gpu'):
        try:
            import torch
            if torch.cuda.is_available() or torch.backends.mps.is_available():
                pytest.skip('Skipping test on GPU')
        except ImportError:
            pass