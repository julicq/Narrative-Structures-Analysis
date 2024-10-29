# bot/telegram_bot.py

import os
from dotenv import load_dotenv
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from narr_mod import StructureType
from service.evaluator import NarrativeEvaluator
from service import initialize_llm
from app.routes import extract_doc_text, extract_text_from_pdf
from shared.config import Config

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.evaluator = None
        self.application = None

    async def setup(self):
        """Инициализация бота и evaluator"""
        # Инициализация LLM и evaluator
        llm = initialize_llm()
        if not llm:
            raise ValueError("Failed to initialize LLM")
        
        self.evaluator = NarrativeEvaluator(llm)
        
        # Создание приложения с использованием builder pattern
        self.application = (
            Application.builder()
            .token(Config.TELEGRAM_TOKEN)
            .build()
        )

        # Регистрация обработчиков
        self.register_handlers()
        
        return self.application

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        await update.message.reply_text(
            "Привет! Я бот для анализа нарративных структур. "
            "Отправь мне текст или документ для анализа."
        )


    def register_handlers(self):
        """Регистрация всех обработчиков команд и сообщений"""
        # Базовые команды
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Обработчики кнопок и текста
        self.application.add_handler(CallbackQueryHandler(self.button))
        self.application.add_handler(
            MessageHandler(
                filters.Regex("^(Выбрать структуру|Помощь|Автоопределение структуры)$"),
                self.handle_button
            )
        )
        
        # Обработчики сообщений
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.analyze_text)
        )
        self.application.add_handler(
            MessageHandler(filters.Document.ALL, self.analyze_file)
        )

        # Обработчик ошибок
        self.application.add_error_handler(self.error_handler)

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"Exception while handling an update: {context.error}")
        if update and update.message:
            await update.message.reply_text(
                "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."
            )

    def get_main_keyboard(self):
        keyboard = [
            [KeyboardButton("Выбрать структуру"), KeyboardButton("Помощь")],
            [KeyboardButton("Автоопределение структуры")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text == "Выбрать структуру":
            await self.choose_structure(update, context)
        elif text == "Помощь":
            await self.help_command(update, context)
        elif text == "Автоопределение структуры":
            context.user_data['selected_structure'] = "Auto-detect"
            await update.message.reply_text("Выбрано автоопределение структуры.")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
        Доступные команды:
        /start - Начать работу с ботом
        /help - Показать это сообщение
        
        Вы можете отправить:
        - Текстовое сообщение
        - Документ (PDF, DOC, DOCX)
        """
        await update.message.reply_text(help_text)

    async def choose_structure(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [[InlineKeyboardButton(StructureType.get_display_name(structure.value), callback_data=structure.value)] 
               for structure in StructureType if structure != StructureType.AUTO_DETECT]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Выберите тип нарративной структуры:', reply_markup=reply_markup)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        context.user_data['selected_structure'] = query.data
        await query.edit_message_text(text=f"Выбрана структура: {query.data}")

    async def analyze_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        structure = context.user_data.get('selected_structure', "Auto-detect")
        await self.process_text(update, context, text, structure)

    async def analyze_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            file = await update.message.document.get_file()
            file_name = update.message.document.file_name
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension not in ['.doc', '.docx', '.pdf', '.txt']:
                await update.message.reply_text("Неподдерживаемый тип файла. Пожалуйста, отправьте doc, docx, pdf или txt файл.")
                return

            await update.message.reply_text(f"Обрабатываю файл {file_name}...")
            
            try:
                await file.download_to_drive(file_name)
                
                if file_extension in ['.doc', '.docx']:
                    text = extract_doc_text(file_name)
                elif file_extension == '.pdf':
                    with open(file_name, 'rb') as f:
                        text = extract_text_from_pdf(f)
                else:  # .txt
                    with open(file_name, 'r', encoding='utf-8') as f:
                        text = f.read()
                        
            finally:
                if os.path.exists(file_name):
                    os.remove(file_name)

            if not text:
                await update.message.reply_text("Не удалось извлечь текст из файла.")
                return

            structure = context.user_data.get('selected_structure', "Auto-detect")
            await self.process_text(update, context, text, structure)
            
        except Exception as e:
            logger.error(f"Error in analyze_file: {e}")
            await update.message.reply_text("Произошла ошибка при обработке файла. Пожалуйста, попробуйте позже.")

    async def process_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, structure: str):
        try:
            await update.message.reply_text("Анализирую текст...")

            if structure == "Auto-detect":
                structure = self.evaluator.classify(text)

            result = self.evaluator.analyze_specific_structure(text, structure)

            response = f"Анализ структуры: {result['structure']}\n\n"
            response += f"Анализ:\n{result['analysis']}\n\n"
            if 'visualization' in result:
                response += f"Визуализация:\n{result['visualization']}"

            if len(response) > 4096:
                for x in range(0, len(response), 4096):
                    await update.message.reply_text(response[x:x+4096])
            else:
                await update.message.reply_text(response)
                
        except Exception as e:
            logger.error(f"Error in process_text: {e}")
            await update.message.reply_text("Произошла ошибка при анализе текста. Пожалуйста, попробуйте позже.")

async def run_bot():
    """Функция для запуска бота"""
    bot = TelegramBot()
    application = await bot.setup()
    
    try:
        await application.initialize()
        await application.start()
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        await application.stop()
