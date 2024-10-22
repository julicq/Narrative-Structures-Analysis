# app.py

from flask import Flask, render_template, request, jsonify
from service import initialize_llm, NarrativeEvaluator

app = Flask(__name__)

# Инициализация LLM и NarrativeEvaluator
llm = initialize_llm()
evaluator = NarrativeEvaluator(llm)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        text = data['text']
        result = evaluator.analyze(text)
        return jsonify(result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
