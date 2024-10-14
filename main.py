### main.py

import os
from flask import Flask, request, jsonify
from service.evaluator import evaluate_narrative
from service.llm import initialize_llm
from app import create_app

app = create_app()
llm = initialize_llm()

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text')
    structure_name = data.get('structure')
    
    if not text or not structure_name:
        return jsonify({"error": "Missing text or structure name"}), 400
    
    result = evaluate_narrative(text, structure_name, llm)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)