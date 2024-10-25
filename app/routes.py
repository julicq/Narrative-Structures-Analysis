# app/routes.py

from flask import Blueprint, request, jsonify, render_template
from narr_mod import get_narrative_structure
from service import initialize_llm, NarrativeEvaluator
from werkzeug.utils import secure_filename
import os
import subprocess
import logging
import platform
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from .constants import STRUCTURE_MAPPING

from service.converter import convert_to_format

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)
llm = initialize_llm()
evaluator = NarrativeEvaluator(llm)

# Список доступных нарративных структур (используется для отображения в интерфейсе)
NARRATIVE_STRUCTURES = list(STRUCTURE_MAPPING.keys())

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


def extract_text_from_pdf_miner(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
        page_interpreter.process_page(page)
    
    text = fake_file_handle.getvalue()
    
    converter.close()
    fake_file_handle.close()
    
    return text

def extract_text_from_txt(file):
    """Извлечение текста из TXT файла"""
    return file.read().decode('utf-8')

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', structures=NARRATIVE_STRUCTURES)

@main_bp.route('/analyze', methods=['POST'])
def analyze_text():
    text = None
    selected_structure = request.form.get('structure')
    
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
                    text = extract_text_from_pdf_miner(file)
                    logger.debug(f"Текст успешно извлечен из PDF файла. Длина текста: {len(text)}")
                    if not text:
                        logger.warning("Извлеченный текст пустой")
                        return jsonify({"error": "Не удалось извлечь текст из PDF файла"}), 400
                except Exception as e:
                    logger.error(f"Ошибка при извлечении текста из PDF файла: {str(e)}")
                    return jsonify({"error": f"Ошибка при обработке PDF файла: {str(e)}"}), 400
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
    
    evaluator = NarrativeEvaluator(llm)

    try:
        if not selected_structure or selected_structure == "Auto-detect":
            structure = evaluator.classify(text)
            if structure == "unknown" or structure not in STRUCTURE_MAPPING:
                structure = "Three-Act Structure"
        else:
            structure = selected_structure

        result = evaluator.analyze_specific_structure(text, structure)
        
        # Теперь result уже содержит всю необходимую информацию
        result['detected_structure'] = structure
        result['structure_name'] = structure
        
        logger.info(f"Analysis completed for structure: {structure}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error during text analysis: {str(e)}")
        return jsonify({"error": str(e)}), 500