# test_flask.py
import os
import sys
import logging
from flask import Flask
from dotenv import load_dotenv

# Добавляем путь к корневой директории проекта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from app import create_app

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_flask_server():
    app = create_app()
    port = int(os.getenv('FLASK_PORT', 5001))
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    try:
        run_flask_server()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down Flask server...")
