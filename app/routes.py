# app/routes.py

from flask import Blueprint, request, jsonify, render_template
from service import initialize_llm, NarrativeEvaluator

main_bp = Blueprint('main', __name__)
llm = initialize_llm()
evaluator = NarrativeEvaluator(llm)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "Missing text"}), 400
    
    result = evaluator.analyze(text)
    return jsonify(result)
