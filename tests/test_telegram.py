from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    user = update.effective_user
    await update.message.reply_text(
        f'Привет, {user.first_name}! 👋\n'
        'Я бот для анализа сценариев. Вот что я умею:\n'
        '/help - показать справку\n'
        '/analyze - начать анализ текста\n'
        'Также вы можете просто отправить мне текст для анализа.'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help."""
    await update.message.reply_text(
        'Справка по использованию бота:\n'
        '1. Отправьте текст для анализа\n'
        '2. Используйте /analyze для подробного анализа\n'
        '3. /settings - настройки анализа'
    )

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /analyze."""
    await update.message.reply_text(
        'Пожалуйста, отправьте текст, который нужно проанализировать.'
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений."""
    text = update.message.text
    # Здесь будет логика анализа текста
    await update.message.reply_text(
        f'Получен текст длиной {len(text)} символов.\n'
        'Начинаю анализ...'
    )

def main():
    """Запуск бота."""
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyze", analyze))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_text
    ))

    # Запускаем бота с дополнительными параметрами
    application.run_polling(
        poll_interval=1.0,
        timeout=30,
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == '__main__':
    main()
