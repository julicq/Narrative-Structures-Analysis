# app/__init__.py

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from shared.config import Config
from app.routes import main_bp
import os

csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Настройка секретного ключа для CSRF
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    
    # Инициализация CSRF защиты
    csrf.init_app(app)

    # Настройка конфигурации
    app.config['UPLOAD_FOLDER'] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        'uploads'
    )
    # Настройка конфигурации
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'doc', 'docx'}
    
    app.register_blueprint(main_bp)

    return app
