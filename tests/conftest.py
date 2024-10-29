# tests/conftest.py
import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,  # Отключаем CSRF для тестов
        "SECRET_KEY": "test_key",
        "SERVER_NAME": "localhost.localdomain"
    })
    
    # Другие настройки тестового окружения
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
