# main.py

from flask import Flask, render_template, request, jsonify, Response
from typing import Union
from shared.config import Config
from http import HTTPStatus
from collections.abc import Mapping
from dashboard.routes import dashboard
from bot.telegram_bot import TelegramBot
import threading

app = Flask(__name__, template_folder='templates')
app.register_blueprint(dashboard, url_prefix='/dashboard')

# Инициализация конфигурации
Config.validate()

# Инициализация бота
bot = TelegramBot()

def run_bot():
    bot.run()

# Запуск бота в отдельном потоке
bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

@app.route('/', methods=['GET', 'POST'])
def index() -> Union[str, tuple[Response, int]]:
    """
    Главный маршрут приложения.
    GET: Возвращает HTML-страницу
    POST: Принимает текст для анализа и возвращает результаты
    """
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data or 'text' not in data:
                return jsonify({
                    'error': 'No text provided'
                }), HTTPStatus.BAD_REQUEST

            text: str = data['text']
            if not text.strip():
                return jsonify({
                    'error': 'Empty text provided'
                }), HTTPStatus.BAD_REQUEST

            result: Mapping = bot.evaluator.analyze(text)
            return jsonify(result), HTTPStatus.OK

        except Exception as e:
            app.logger.error(f"Error processing request: {str(e)}")
            return jsonify({
                'error': 'Internal server error'
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    return render_template('index.html')

@app.route('/dashboard')
def dashboard_index():
    return render_template('dashboard/index.html')

@app.errorhandler(404)
def not_found(error) -> tuple[Response, int]:
    """Обработчик ошибки 404"""
    return jsonify({'error': 'Not found'}), HTTPStatus.NOT_FOUND

@app.errorhandler(500)
def internal_error(error) -> tuple[Response, int]:
    """Обработчик ошибки 500"""
    app.logger.error(f'Server Error: {error}')
    return jsonify({'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.DEBUG)
