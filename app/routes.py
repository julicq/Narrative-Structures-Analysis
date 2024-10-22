# app/routes.py

from flask import Blueprint, request, jsonify
from service.evaluator import evaluate_narrative
from service.llm import initialize_llm

main_bp = Blueprint('main', __name__)
llm = initialize_llm()

@main_bp.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "Missing text"}), 400
    
    result = evaluate_narrative(text, "four_act", llm)
    return jsonify(result)
