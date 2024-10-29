# app/file_handlers/pdf_handler.py

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import logging
from typing import BinaryIO, Union, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file: Union[str, Path, BinaryIO]) -> Optional[str]:
    """Извлекает текст из PDF файла.
    
    Args:
        file: Путь к PDF файлу или файловый объект в бинарном режиме
        
    Returns:
        str: Извлеченный текст или None в случае ошибки
        
    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если файл не является PDF или не может быть прочитан
        IOError: При ошибках ввода/вывода
    """
    # Если передан путь к файлу, открываем его
    if isinstance(file, (str, Path)):
        file_path = Path(file)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        file = open(file_path, 'rb')
        need_close = True
    else:
        need_close = False

    try:
        resource_manager = PDFResourceManager()
        output_string = StringIO()
        converter = TextConverter(
            resource_manager, 
            output_string,
            laparams=LAParams(
                line_margin=0.5,
                char_margin=2.0,
                word_margin=0.1,
                boxes_flow=0.5,
                detect_vertical=True
            )
        )
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        
        for page in PDFPage.get_pages(
            file,
            caching=True,
            check_extractable=True
        ):
            page_interpreter.process_page(page)
        
        text = output_string.getvalue().strip()
        
        return text if text else None

    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise
    
    finally:
        converter.close()
        output_string.close()
        if need_close:
            file.close()
