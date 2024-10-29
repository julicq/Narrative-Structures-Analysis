# run_services.py

import asyncio
import logging
from flask import Flask, request
from app import create_app
from bot.telegram_bot import TelegramBot
from threading import Thread
from werkzeug.serving import make_server

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class FlaskServerThread(Thread):
    def __init__(self, app, host='0.0.0.0', port=5001):
        super().__init__()
        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        logger.info('Starting Flask server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

class ServiceManager:
    def __init__(self):
        self._initialized = False
        self._running = False
        self._stop_event = asyncio.Event()
        self.bot = None
        self.flask_server = None
        self.flask_thread = None

    async def init_services(self):
        if self._initialized:
            return

        logger.info("Initializing services...")
        
        # Инициализация Flask
        logger.info("Creating Flask application...")
        self.flask_server = create_app()
        
        # Инициализация бота
        logger.info("Initializing Telegram bot...")
        self.bot = TelegramBot()
        await self.bot.setup()
        
        self._initialized = True
        logger.info("Services initialized successfully")

    async def run_services(self):
        """Основной метод запуска всех сервисов"""
        if not self._initialized:
            await self.init_services()
        
        self._running = True
        
        try:
            # Запуск Flask в отдельном потоке
            self.flask_thread = FlaskServerThread(self.flask_server)
            self.flask_thread.daemon = True
            self.flask_thread.start()
            logger.info("Flask server thread started")
            
            # Запуск бота
            logger.info("Starting Telegram bot...")
            await self.bot.start_polling()
            
            # Ждем сигнала остановки
            while not self._stop_event.is_set():
                await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"Error running services: {e}")
            raise
        finally:
            self._running = False
            await self.shutdown()

    async def shutdown(self):
        """Корректное завершение работы всех сервисов"""
        if not self._running:
            return
            
        logger.info("Initiating shutdown sequence...")
        
        # Останавливаем бота
        if self.bot:
            try:
                await self.bot.stop()
                logger.info("Telegram bot stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping Telegram bot: {e}")
            finally:
                self.bot = None

        # Останавливаем Flask сервер
        if self.flask_thread:
            try:
                self.flask_thread.shutdown()
                self.flask_thread.join(timeout=5)
                logger.info("Flask server stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping Flask server: {e}")
            finally:
                self.flask_thread = None

        self._initialized = False
        self._running = False
        logger.info("Shutdown completed")

async def main():
    """Точка входа для запуска сервисов"""
    service_manager = ServiceManager()
    try:
        await service_manager.run_services()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        service_manager._stop_event.set()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await service_manager.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application crashed: {e}")
