# test_telegram.py

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
        
    def setup_handlers(self):
        # Добавляем базовые обработчики для тестирования
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
    async def start_command(self, update: Update, context):
        await update.message.reply_text('Привет! Бот запущен и работает.')
        
    async def handle_message(self, update: Update, context):
        await update.message.reply_text(f'Получено сообщение: {update.message.text}')
        
    async def start(self):
        logger.info("Starting Telegram bot...")
        await self.application.initialize()
        await self.application.start()
        await self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    async def stop(self):
        logger.info("Stopping Telegram bot...")
        await self.application.stop()
        await self.application.shutdown()

async def main():
    bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))
    try:
        await bot.start()
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await bot.stop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down Telegram bot...")
