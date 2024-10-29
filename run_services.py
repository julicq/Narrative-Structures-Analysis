# run_services.py

import asyncio
from flask import Flask
from telegram import Update
from werkzeug.serving import make_server
from bot.telegram_bot import TelegramBot
from telegram.ext import Application, CommandHandler
from app import create_app
from shared.config import Config
import logging
import threading
import signal

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class FlaskServer(threading.Thread):
    def __init__(self, app: Flask):
        super().__init__()
        self.app = app
        self.server = None
        self.daemon = True
        self._stop_event = threading.Event()

    def run(self):
        try:
            self.server = make_server('0.0.0.0', Config.FLASK_PORT, self.app)
            logger.info(f"Flask server starting on port {Config.FLASK_PORT}")
            self.server.serve_forever()
        except Exception as e:
            logger.error(f"Flask server error: {e}")

    def stop(self):
        self._stop_event.set()
        if self.server:
            self.server.shutdown()
            logger.info("Flask server stopped")

class ServiceManager:
    def __init__(self):
        self.flask_server = None
        self.application = None
        self._stop_event = asyncio.Event()

    def setup_signal_handlers(self):
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, self._handle_signal)

    def _handle_signal(self, signum, frame):
        logger.info(f"Received signal {signum}")
        if self.flask_server:
            self.flask_server.stop()
        asyncio.get_event_loop().create_task(self._shutdown())

    async def _shutdown(self):
        if self.application:
            await self.application.stop()
            await self.application.shutdown()
        self._stop_event.set()

    async def start_services(self):
        try:
            # Запуск Flask
            app = create_app()
            self.flask_server = FlaskServer(app)
            self.flask_server.start()

            # Запуск Telegram бота
            bot = TelegramBot()
            self.application = (
                Application.builder()
                .token(Config.TELEGRAM_TOKEN)
                .build()
            )
            
            # Регистрация обработчиков
            self.application.add_handler(CommandHandler("start", bot.start_command))
            self.application.add_handler(CommandHandler("help", bot.help_command))

            # Инициализация и запуск бота
            await self.application.initialize()
            await self.application.start()
            logger.info("Starting Telegram bot polling...")
            
            # Ожидаем завершения работы
            await self._stop_event.wait()
            
        except Exception as e:
            logger.error(f"Error in start_services: {e}")
            raise
        finally:
            if self.application:
                await self.application.stop()
            if self.flask_server:
                self.flask_server.stop()

async def main():
    service_manager = ServiceManager()
    service_manager.setup_signal_handlers()
    
    try:
        await service_manager.start_services()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
