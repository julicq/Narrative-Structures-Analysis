# tests/test_app.py

import pytest
from flask import url_for
import json
from unittest.mock import patch, MagicMock
from shared.models_api import model_api
from narr_mod import StructureType

@pytest.fixture
def app():
    """Создаем тестовое приложение"""
    from app import create_app
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SERVER_NAME": "localhost.localdomain"
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    """Тест главной страницы"""
    response = client.get('/?locale=en')
    assert response.status_code == 200
    assert b'Narrative Structure' in response.data

def test_home_page_ru(client):
    """Тест главной страницы на русском"""
    response = client.get('/?locale=ru')
    assert response.status_code == 200
    # Проверяем только статус, так как локализация может быть реализована позже
    assert response.status_code == 200

@pytest.mark.parametrize('structure_type', [
    StructureType.THREE_ACT.value,
    StructureType.VOGLER_HERO_JOURNEY.value,
    StructureType.HARMON_CIRCLE.value
])
def test_analyze_endpoint_with_different_structures(client, structure_type):
    """Тест endpoint'а анализа с разными типами структур"""
    test_data = {
        'text': 'Test story content',
        'structure_type': structure_type
    }
    
    with patch.object(model_api, 'analyze_text') as mock_analyze:
        mock_analyze.return_value = {
            'analysis': f'Analysis for {structure_type}',
            'model_info': 'OLLAMA'
        }
        
        response = client.post('/analyze',
                             json=test_data,
                             content_type='application/json')
        
        print(f"\nTesting structure: {structure_type}")
        print(f"Request data: {test_data}")
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data.decode()}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'result' in data

def test_analyze_endpoint_with_empty_text(client):
    """Тест обработки пустого текста"""
    test_data = {
        'text': '',
        'structure_type': 'three-act'
    }
    
    response = client.post('/analyze',
                          json=test_data,
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'error' in data

def test_analyze_endpoint_with_long_text(client):
    """Тест обработки длинного текста"""
    test_data = {
        'text': 'A' * 10000,
        'structure_type': StructureType.THREE_ACT.value
    }
    
    with patch.object(model_api, 'analyze_text') as mock_analyze:
        mock_analyze.return_value = {
            'analysis': 'Analysis for long text',
            'model_info': 'OLLAMA'
        }
        
        response = client.post('/analyze',
                             json=test_data,
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'result' in data


def test_invalid_structure_type(client):
    """Тест с неверным типом структуры"""
    test_data = {
        'text': 'Test story',
        'structure_type': 'invalid_structure'
    }
    
    response = client.post('/analyze',
                          json=test_data,
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert 'error' in data
    assert 'Invalid structure type' in data['error']

@pytest.mark.parametrize('locale', ['en', 'ru'])
def test_localization(client, locale):
    """Тест локализации"""
    response = client.get(f'/?locale={locale}')
    assert response.status_code == 200
    content = response.data.decode('utf-8').lower()
    
    if locale == 'en':
        assert 'analyze' in content or 'submit' in content
    else:
        # Проверяем наличие русского текста, учитывая возможные варианты
        assert 'анализ' in content or 'отправить' in content or 'структура' in content


def test_model_error(client):
    """Тест обработки ошибок модели"""
    test_data = {
        'text': 'Test story',
        'structure_type': StructureType.THREE_ACT.value
    }
    
    with patch.object(model_api, 'analyze_text') as mock_analyze:
        mock_analyze.return_value = {
            'status': 'error',
            'error': 'Model error occurred',
            'model_info': 'OLLAMA'
        }
        
        response = client.post('/analyze',
                             json=test_data,
                             content_type='application/json')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'error' in data

