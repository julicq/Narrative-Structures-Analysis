# bot/telegram_bot.py

import asyncio
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
        """Инициализация бота"""
        # Инициализация LLM и evaluator
        llm = initialize_llm()
        if not llm:
            raise ValueError("Failed to initialize LLM")
        
        self.evaluator = NarrativeEvaluator(llm)
        
        # Создание приложения
        self.application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        
        # Регистрация обработчиков
        self.register_handlers()
        
        # Инициализация приложения
        await self.application.initialize()
        await self.application.start()
        
        return self.application

    def register_handlers(self):
        """Регистрация обработчиков команд"""
        if not self.application:
            raise RuntimeError("Application not initialized")

        # Основные обработчики
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.handle_message
        ))
        self.application.add_handler(CallbackQueryHandler(self.button))
        
        # Обработчик документов (файлов)
        self.application.add_handler(MessageHandler(
            filters.Document.ALL, 
            self.analyze_file
        ))
        
        # Обработчик ошибок
        self.application.add_error_handler(self.error_handler)

    def get_main_keyboard(self):
        """Создание основной клавиатуры"""
        keyboard = [
            [KeyboardButton("Выбрать структуру"), KeyboardButton("Помощь")],
            [KeyboardButton("Автоопределение структуры")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        keyboard = self.get_main_keyboard()
        await update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n"
            "Я бот для анализа нарративных структур.\n"
            "Выберите действие или отправьте текст для анализа:",
            reply_markup=keyboard
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = (
            "🤖 *Как использовать бота:*\n\n"
            "1. Отправьте текст для быстрого анализа\n"
            "2. Используйте команды:\n"
            "   /start - начать работу\n"
            "   /help - показать эту справку\n\n"
            "📄 *Поддерживаемые форматы файлов:*\n"
            "• TXT - текстовые файлы\n"
            "• DOC/DOCX - документы Word\n"
            "• PDF - PDF документы\n\n"
            "Вы также можете:\n"
            "• Выбрать конкретную структуру для анализа\n"
            "• Использовать автоопределение структуры"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        text = update.message.text
        
        # Обработка кнопок меню
        if text in ["Выбрать структуру", "Помощь", "Автоопределение структуры"]:
            await self.handle_button(update, context)
            return

        try:
            # Отправляем сообщение о начале обработки
            processing_message = await update.message.reply_text(
                "🔄 Анализирую текст... Это может занять некоторое время."
            )
            
            structure = context.user_data.get('selected_structure', "Auto-detect")
            await self.process_text(update, context, text, structure)
            await processing_message.delete()
                
        except Exception as e:
            error_message = f"❌ Произошла ошибка при обработке сообщения: {str(e)}"
            await update.message.reply_text(error_message)
            logger.error(f"Error in handle_message: {e}")

    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на текстовые кнопки"""
        text = update.message.text
        if text == "Выбрать структуру":
            await self.choose_structure(update, context)
        elif text == "Помощь":
            await self.help_command(update, context)
        elif text == "Автоопределение структуры":
            context.user_data['selected_structure'] = "Auto-detect"
            await update.message.reply_text(
                "Выбрано автоопределение структуры.\n"
                "Отправьте текст или файл для анализа."
            )

    async def choose_structure(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ меню выбора структуры"""
        keyboard = [
            [InlineKeyboardButton(
                StructureType.get_display_name(structure.value),
                callback_data=structure.value
            )]
            for structure in StructureType if structure != StructureType.AUTO_DETECT
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            'Выберите тип нарративной структуры:',
            reply_markup=reply_markup
        )

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик inline кнопок"""
        query = update.callback_query
        await query.answer()
        context.user_data['selected_structure'] = query.data
        await query.edit_message_text(text=f"Выбрана структура: {query.data}")

    async def analyze_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик файлов"""
        try:
            file = await update.message.document.get_file()
            file_name = update.message.document.file_name
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension not in ['.doc', '.docx', '.pdf', '.txt']:
                await update.message.reply_text(
                    "Неподдерживаемый тип файла. Пожалуйста, отправьте doc, docx, pdf или txt файл."
                )
                return

            processing_message = await update.message.reply_text(f"Обрабатываю файл {file_name}...")
            
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
                await processing_message.edit_text("Не удалось извлечь текст из файла.")
                return

            structure = context.user_data.get('selected_structure', "Auto-detect")
            await self.process_text(update, context, text, structure)
            await processing_message.delete()
            
        except Exception as e:
            logger.error(f"Error in analyze_file: {e}")
            await update.message.reply_text(
                "Произошла ошибка при обработке файла. Пожалуйста, попробуйте позже."
            )

    async def process_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, structure: str):
        """Обработка текста и отправка результатов анализа"""
        try:
            if structure == "Auto-detect":
                structure = self.evaluator.classify(text)

            result = self.evaluator.analyze_specific_structure(text, structure)

            response = f"Анализ структуры: {result['structure']}\n\n"
            response += f"Анализ:\n{result['analysis']}\n\n"
            if 'visualization' in result:
                response += f"Визуализация:\n{result['visualization']}"

            # Разбиваем длинные сообщения на части
            if len(response) > 4096:
                for x in range(0, len(response), 4096):
                    await update.message.reply_text(response[x:x+4096])
            else:
                await update.message.reply_text(response)
                
        except Exception as e:
            logger.error(f"Error in process_text: {e}")
            await update.message.reply_text(
                "Произошла ошибка при анализе текста. Пожалуйста, попробуйте позже."
            )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"Exception while handling an update: {context.error}")
        if update and update.message:
            await update.message.reply_text(
                "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."
            )

async def run_bot():
    """Асинхронный запуск бота"""
    bot = TelegramBot()
    await bot.setup()
    await bot.application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

def main():
    """Точка входа"""
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == '__main__':
    main()
