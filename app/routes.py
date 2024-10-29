# app/routes.py

from flask import Blueprint, request, jsonify, render_template
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
import os
import logging
from shared.config import Config
from shared.models_api import model_api
from .file_handlers.doc_handler import extract_doc_text
from .file_handlers.pdf_handler import extract_text_from_pdf
from narr_mod import StructureType

logger = logging.getLogger(__name__)
main_bp = Blueprint('main', __name__)

# Список доступных нарративных структур
NARRATIVE_STRUCTURES = [structure.value for structure in StructureType if structure != StructureType.AUTO_DETECT]

ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def ensure_upload_dir():
    """Создает директорию для загрузки файлов, если она не существует"""
    upload_dir = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return upload_dir

def is_allowed_file(filename):
    """Проверяет допустимость расширения файла"""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/', methods=['GET'])
def index():
    """Главная страница приложения"""
    locale = request.args.get('locale', 'en')
    return render_template('index.html', 
                         structures=NARRATIVE_STRUCTURES, 
                         csrf_token=generate_csrf(),
                         locale=locale)

@main_bp.route('/analyze', methods=['POST'])
def analyze_text():
    """Endpoint для анализа текста"""
    try:
        text = None
        selected_structure = None

        if request.is_json:
            data = request.get_json()
            if not data:
                return jsonify({
                    "status": "error",
                    "error": "Invalid JSON data"
                }), 400
            text = data.get('text', '').strip()
            selected_structure = data.get('structure_type', StructureType.THREE_ACT.value).strip()
        else:
            selected_structure = request.form.get('structure', StructureType.THREE_ACT.value).strip()
            text = request.form.get('text', '').strip()
            
            if not text and 'file' in request.files:
                file = request.files['file']
                if file and file.filename:
                    if not is_allowed_file(file.filename):
                        return jsonify({
                            "status": "error",
                            "error": f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
                        }), 400

                    if file.content_length and file.content_length > MAX_FILE_SIZE:
                        return jsonify({
                            "status": "error",
                            "error": f"File size exceeds maximum limit of {MAX_FILE_SIZE/1024/1024}MB"
                        }), 400

                    filename = secure_filename(file.filename)
                    file_extension = os.path.splitext(filename)[1].lower()
                    
                    try:
                        if file_extension == '.doc':
                            upload_dir = ensure_upload_dir()
                            file_path = os.path.join(upload_dir, filename)
                            file.save(file_path)
                            try:
                                text = extract_doc_text(file_path)
                            finally:
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                        
                        elif file_extension == '.pdf':
                            text = extract_text_from_pdf(file)
                        
                        elif file_extension == '.txt':
                            text = file.read().decode('utf-8')
                        
                    except Exception as e:
                        logger.error(f"Error processing file {filename}: {str(e)}")
                        return jsonify({
                            "status": "error",
                            "error": f"Error processing file: {str(e)}"
                        }), 500

        if not text:
            return jsonify({
                "status": "error",
                "error": "No text provided. Please enter text or upload a file."
            }), 400

        # Проверяем, что структура валидна
        if selected_structure not in NARRATIVE_STRUCTURES:
            return jsonify({
                "status": "error",
                "error": f"Invalid structure type. Allowed types: {', '.join(NARRATIVE_STRUCTURES)}"
            }), 400

        logger.info(f"Starting analysis with structure type: {selected_structure}")
        logger.info(f"Text length: {len(text)} characters")

        result = model_api.analyze_text(
            text=text,
            structure_type=selected_structure
        )
        
        if isinstance(result, dict) and result.get('status') == 'error':
            return jsonify({
                "status": "error",
                "error": result.get('error', 'Model error occurred'),
                "model_info": result.get('model_info', 'Unknown')
            }), 500
            
        return jsonify({
            "status": "success",
            "result": result
        }), 200
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint для проверки состояния сервиса"""
    return jsonify({
        'status': 'healthy',
        'active_model': Config.ACTIVE_MODEL.value,
        'supported_structures': NARRATIVE_STRUCTURES
    })

@main_bp.route('/test_ollama', methods=['GET'])
def test_ollama():
    """Endpoint для проверки соединения с Ollama"""
    try:
        result = model_api.model.invoke("Test connection to Ollama. Reply with 'OK'.")
        return jsonify({
            'status': 'success',
            'response': str(result),
            'model_info': model_api.get_model_info()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'model_info': model_api.get_model_info()
        }), 500

@main_bp.errorhandler(413)
def request_entity_too_large(error):
    """Обработчик ошибки превышения размера файла"""
    return jsonify({
        'status': 'error',
        'error': f'File too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB'
    }), 413

@main_bp.errorhandler(500)
def internal_server_error(error):
    """Обработчик внутренних ошибок сервера"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'status': 'error',
        'error': 'Internal server error occurred'
    }), 500
