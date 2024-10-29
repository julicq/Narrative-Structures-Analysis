# app/file_handlers/doc_handler.py

import platform
import subprocess
import os
import logging
from docx import Document
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_doc_text(file_path):
    """Извлечение текста из .doc файла
    
    Args:
        file_path (str): Путь к .doc файлу
        
    Returns:
        str: Извлеченный текст или None в случае ошибки
        
    Raises:
        FileNotFoundError: Если файл не найден
        subprocess.SubprocessError: При ошибке конвертации
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        if platform.system() == 'Darwin':  # MacOS
            txt_path = file_path + '.txt'
            subprocess.run(['textutil', '-convert', 'txt', '-output', txt_path, file_path], 
                        check=True)
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            os.remove(txt_path)
            return text
        else:  # Linux/Unix
            result = subprocess.run(['antiword', file_path], 
                                capture_output=True, 
                                text=True,
                                check=True)
            return result.stdout
    except subprocess.SubprocessError as e:
        logger.error(f"Error converting file {file_path}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error processing file {file_path}: {str(e)}")
        return None

def extract_docx_text(file_path):
    """Извлечение текста из .docx файла
    
    Args:
        file_path (str): Путь к .docx файлу
        
    Returns:
        str: Извлеченный текст или None в случае ошибки
        
    Raises:
        FileNotFoundError: Если файл не найден
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        doc = Document(file_path)
        full_text = []
        
        # Извлекаем текст из параграфов
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text)
        
        # Извлекаем текст из таблиц
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        full_text.append(cell.text)
        
        return '\n'.join(full_text)
    except Exception as e:
        logger.error(f"Error processing DOCX file {file_path}: {str(e)}")
        return None

def extract_text(file_path):
    """Универсальная функция для извлечения текста из .doc или .docx файлов
    
    Args:
        file_path (str): Путь к файлу
        
    Returns:
        str: Извлеченный текст или None в случае ошибки
        
    Raises:
        ValueError: Если формат файла не поддерживается
        FileNotFoundError: Если файл не найден
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    extension = file_path.suffix.lower()
    
    if extension == '.doc':
        return extract_doc_text(str(file_path))
    elif extension == '.docx':
        return extract_docx_text(str(file_path))
    else:
        error_msg = f"Unsupported file format: {extension}"
        logger.error(error_msg)
        raise ValueError(error_msg)
