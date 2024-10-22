# app/__init__.py

from flask import Flask
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация CORS
    CORS(app)

    # Инициализация других расширений Flask, если они есть
    # например, db = SQLAlchemy(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    @app.route('/health')
    def health_check():
        return {'status': 'OK'}, 200

    return app
