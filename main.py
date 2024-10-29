# app.py

from flask import Flask, render_template, request, jsonify, Response
from typing import Union
from service import initialize_llm, NarrativeEvaluator
from http import HTTPStatus
from collections.abc import Mapping

app = Flask(__name__)

# Инициализация LLM и NarrativeEvaluator
llm = initialize_llm()
evaluator = NarrativeEvaluator(llm)

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

            result: Mapping = evaluator.analyze(text)
            return jsonify(result), HTTPStatus.OK

        except Exception as e:
            app.logger.error(f"Error processing request: {str(e)}")
            return jsonify({
                'error': 'Internal server error'
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    return render_template('index.html')

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
    app.run(debug=True)
