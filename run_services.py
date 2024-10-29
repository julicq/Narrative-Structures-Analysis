# run_services.py

import asyncio
import logging
import signal
import threading
from flask import Flask
from werkzeug.serving import make_server
from bot.telegram_bot import TelegramBot
from app import create_app
from shared.config import Config
import nest_asyncio

# Применяем nest_asyncio для решения проблем с вложенными event loops
nest_asyncio.apply()

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
        self.bot = None
        self._stop_event = None

    async def init_services(self):
        self._stop_event = asyncio.Event()
        
        # Инициализация Flask
        logger.info("Starting Flask server...")
        app = create_app()
        self.flask_server = FlaskServer(app)
        self.flask_server.start()

        # Инициализация Telegram бота
        logger.info("Initializing Telegram bot...")
        self.bot = TelegramBot()
        self.bot.application = await self.bot.setup()

    async def run_services(self):
        try:
            logger.info("Starting bot polling...")
            await self.bot.application.initialize()
            await self.bot.application.start()
            await self.bot.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        except Exception as e:
            logger.error(f"Error in services: {e}")
            raise
        finally:
            await self.shutdown()

    async def shutdown(self):
        logger.info("Shutting down services...")
        
        if self.flask_server:
            self.flask_server.stop()

        if self.bot and self.bot.application:
            try:
                await self.bot.application.stop()
            except Exception as e:
                logger.error(f"Error stopping bot: {e}")

        logger.info("All services stopped")

def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}")
    if hasattr(signal_handler, 'loop'):
        signal_handler.loop.create_task(shutdown_services())

async def shutdown_services():
    if hasattr(shutdown_services, 'manager'):
        await shutdown_services.manager.shutdown()

async def main():
    try:
        manager = ServiceManager()
        shutdown_services.manager = manager
        signal_handler.loop = asyncio.get_running_loop()
        
        # Установка обработчиков сигналов
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        await manager.init_services()
        await manager.run_services()

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise
    finally:
        await manager.shutdown()

def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application shutdown by keyboard interrupt")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        logger.info("Application stopped")

if __name__ == '__main__':
    run()
