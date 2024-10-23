# app/routes.py

from flask import Blueprint, request, jsonify, render_template
from service import initialize_llm, NarrativeEvaluator
from werkzeug.utils import secure_filename
import os
import subprocess
import logging
import platform
import io
from PyPDF2 import PdfReader

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)
llm = initialize_llm()
evaluator = NarrativeEvaluator(llm)

def extract_doc_text(file_path):
    """Извлечение текста из .doc файла"""
    if platform.system() == 'Darwin':  # MacOS
        txt_path = file_path + '.txt'
        subprocess.run(['textutil', '-convert', 'txt', '-output', txt_path, file_path])
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
        os.remove(txt_path)
        return text
    else:  # Linux/Unix
        result = subprocess.run(['antiword', file_path], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else None

def extract_text_from_pdf(file):
    """Извлечение текста из PDF файла"""
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(file):
    """Извлечение текста из TXT файла"""
    return file.read().decode('utf-8')

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/analyze', methods=['POST'])
def analyze_text():
    text = None
    
    # Проверяем, есть ли текст в форме
    form_text = request.form.get('text')
    if form_text:
        text = form_text
        logger.debug("Text received from form")
    
    # Если текста в форме нет, проверяем наличие файла
    if not text and 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1].lower()
            
            if file_extension == '.doc':
                file_path = os.path.join('uploads', filename)
                if not os.path.exists('uploads'):
                    os.makedirs('uploads')
                file.save(file_path)
                try:
                    text = extract_doc_text(file_path)
                    logger.debug("Text extracted from uploaded .doc file")
                except Exception as e:
                    logger.error(f"Error extracting text from .doc file: {str(e)}")
                finally:
                    if os.path.exists(file_path):
                        os.remove(file_path)
            elif file_extension == '.pdf':
                try:
                    text = extract_text_from_pdf(file)
                    logger.debug("Text extracted from uploaded PDF file")
                except Exception as e:
                    logger.error(f"Error extracting text from PDF file: {str(e)}")
            elif file_extension == '.txt':
                try:
                    text = extract_text_from_txt(file)
                    logger.debug("Text extracted from uploaded TXT file")
                except Exception as e:
                    logger.error(f"Error extracting text from TXT file: {str(e)}")
            else:
                logger.error(f"Unsupported file type: {file_extension}")
                return jsonify({"error": "Unsupported file type"}), 400
    
    if not text:
        return jsonify({"error": "No text could be extracted from form or file"}), 400
    
    try:
        result = evaluator.analyze(text)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error during text analysis: {str(e)}")
        return jsonify({"error": "An error occurred during analysis"}), 500
