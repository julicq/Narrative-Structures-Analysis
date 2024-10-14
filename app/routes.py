from flask import Blueprint, request, jsonify
from service.evaluator import evaluate_narrative
from service.llm import initialize_llm

main_bp = Blueprint('main', __name__)
llm = initialize_llm()

@main_bp.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text')
    structure_name = data.get('structure')
    
    if not text or not structure_name:
        return jsonify({"error": "Missing text or structure name"}), 400
    
    result = evaluate_narrative(text, structure_name, llm)
    return jsonify(result)
