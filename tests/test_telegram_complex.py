from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import logging
from dotenv import load_dotenv
import os
import re
from typing import Dict, List, Tuple
import json

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Базовые паттерны для анализа
DIALOGUE_PATTERN = r'["\'].*?["\']|[-—].*?[.!?]'
SCENE_HEADER_PATTERN = r'^(INT\.|EXT\.).+$'
ACTION_PATTERN = r'^[A-Z][^a-z]*$'

class TextAnalyzer:
    @staticmethod
    def analyze_text(text: str) -> Dict:
        """Базовый анализ текста."""
        # Подсчет базовых метрик
        words = len(text.split())
        sentences = len(re.findall(r'[.!?]+', text))
        dialogues = len(re.findall(DIALOGUE_PATTERN, text, re.MULTILINE))
        scenes = len(re.findall(SCENE_HEADER_PATTERN, text, re.MULTILINE))
        
        # Анализ структуры
        paragraphs = text.count('\n\n') + 1
        
        return {
            "words": words,
            "sentences": sentences,
            "dialogues": dialogues,
            "scenes": scenes,
            "paragraphs": paragraphs,
            "avg_words_per_sentence": round(words/max(sentences, 1), 2)
        }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Помощь", callback_data='help')],
        [InlineKeyboardButton("Начать анализ", callback_data='analyze')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f'Здравствуйте, {user.first_name}! 👋\n'
        'Я бот для анализа сценариев и текстов. Я могу:\n'
        '• Анализировать структуру текста\n'
        '• Находить диалоги и сцены\n'
        '• Предоставлять базовую статистику\n\n'
        'Выберите действие или отправьте текст для анализа:',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help."""
    help_text = (
        'Как использовать бот:\n\n'
        '1. Отправьте текст для быстрого анализа\n'
        '2. Используйте команды:\n'
        '   /analyze - начать подробный анализ\n'
        '   /stats - показать статистику\n'
        '   /settings - настройки анализа\n\n'
        'Поддерживаемые форматы:\n'
        '• Обычный текст\n'
        '• Сценарии\n'
        '• Диалоги'
    )
    await update.message.reply_text(help_text)

async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /analyze."""
    keyboard = [
        [
            InlineKeyboardButton("Базовый анализ", callback_data='basic_analysis'),
            InlineKeyboardButton("Подробный анализ", callback_data='detailed_analysis')
        ],
        [InlineKeyboardButton("Отмена", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        'Выберите тип анализа:',
        reply_markup=reply_markup
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений."""
    text = update.message.text
    
    # Выполняем базовый анализ
    analysis = TextAnalyzer.analyze_text(text)
    
    # Формируем ответ
    response = (
        f'📊 Результаты анализа:\n\n'
        f'📝 Слов: {analysis["words"]}\n'
        f'📈 Предложений: {analysis["sentences"]}\n'
        f'💬 Диалогов: {analysis["dialogues"]}\n'
        f'🎬 Сцен: {analysis["scenes"]}\n'
        f'📋 Параграфов: {analysis["paragraphs"]}\n'
        f'📊 Среднее количество слов в предложении: {analysis["avg_words_per_sentence"]}\n\n'
        f'Для подробного анализа используйте команду /analyze'
    )
    
    await update.message.reply_text(response)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help':
        await help_command(update, context)
    elif query.data == 'analyze':
        await analyze_command(update, context)
    elif query.data == 'cancel':
        await query.edit_message_text('Операция отменена.')

def main():
    """Запуск бота."""
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyze", analyze_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_text
    ))

    # Запускаем бота
    application.run_polling(
        poll_interval=1.0,
        timeout=30,
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == '__main__':
    main()
