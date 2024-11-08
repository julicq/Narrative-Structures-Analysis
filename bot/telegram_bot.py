# bot/telegram_bot.py

import os
from typing import Dict, Any
from dotenv import load_dotenv
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes
)
from narr_mod import StructureType
from service.evaluator import NarrativeEvaluator
from service import initialize_llm
from shared.config import Config
import tempfile
from pathlib import Path
from app.file_handlers.doc_handler import extract_text as extract_doc_text
from app.file_handlers.pdf_handler import extract_text_from_pdf
from db.database import Database
from service.balance_service import BalanceService

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
        self.application = None
        self._initialized = False
        self._running = False
        self.evaluator = None
        self.user_states: Dict[int, Dict[str, Any]] = {}
        self.user_data: Dict[int, Dict[str, Any]] = {}
        self.DEFAULT_TOKEN_BALANCE = 100_000
        self.PAGE_LIMIT = 50
        self.TOKENS_PER_PAGE = 500
        self.db = Database()
        self.balance_service = BalanceService()
        self.admin_id = 218293337

    def setup(self):
        """Синхронная инициализация бота"""
        if self._initialized:
            return
            
        logger.info("Setting up Telegram bot...")
        
        # Инициализация LLM и evaluator с поддержкой GigaChat
        try:
            llm = initialize_llm()
            gigachat_token = os.getenv('GIGACHAT_TOKEN')
            
            self.evaluator = NarrativeEvaluator(
                llm=llm,
                gigachat_token=gigachat_token
            )
            logger.info("Evaluator initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM and evaluator: {e}")
            raise ValueError("Failed to initialize LLM and evaluator")
    
        self.application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        
        # Регистрируем обработчики
        self.register_handlers()
        self._initialized = True
        logger.info("Telegram bot setup completed")


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
            self.handle_document
        ))
        
        # Обработчик ошибок
        self.application.add_error_handler(self.error_handler)

        # Баланс
        self.application.add_handler(CommandHandler("balance", self.balance_command))
        self.application.add_handler(CommandHandler("limits", self.limits_command))
        self.application.add_handler(CommandHandler("add_tokens", self.add_tokens_request))
        self.application.add_handler(CommandHandler("approve_tokens", self.approve_tokens_command, filters=filters.User(user_id=self.admin_id)))


    def send_welcome(self, message):
        welcome_message = Config.get_bot_message('welcome')
        self.bot.reply_to(message, welcome_message)

    def send_help(self, message):
        help_message = Config.get_bot_message('help')
        self.bot.reply_to(message, help_message)
        
    def run(self):
        """Синхронный метод запуска бота"""
        if not self._initialized:
            self.setup()
        
        logger.info("Starting bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

        try:
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        finally:
            self.db.close()

    async def start_polling(self):
        """Запуск бота"""
        if not self._initialized:
            await self.setup()
                
        logger.info("Starting bot polling...")
        self._running = True
        
        # Больше не нужно вызывать initialize() и start() отдельно
        await self.application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            close_loop=False  # Важный параметр!
    )

    def get_main_keyboard(self):
        """Создание основной клавиатуры"""
        keyboard = [
            [KeyboardButton("Выбрать структуру"), KeyboardButton("Помощь")],
            [KeyboardButton("Автоопределение структуры")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        if not update.effective_user:
            return
                
        user = update.effective_user
        user_id = user.id
        user_data = self.db.get_user_data(user_id)
        chat_id = update.effective_chat.id
        # Если у пользователя нет баланса, устанавливаем значение по умолчанию
        if "token_balance" not in user_data:
            self.db.update_user_balance(user_id, self.DEFAULT_TOKEN_BALANCE)
            balance = self.DEFAULT_TOKEN_BALANCE
        else:
            balance = user_data["token_balance"]
        if balance == 0:
            self.db.update_user_balance(user_id, self.DEFAULT_TOKEN_BALANCE)
        logger.info(f"Start command received from user {user.id} in chat {chat_id}")
        
        keyboard = self.get_main_keyboard()
        await update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n"
            "Я бот для анализа нарративных структур в сценариях.\n"
            "Выберите действие в нижнем меню или отправьте текст для анализа (имейте в виду, что в одном сообщении можно отправить максимум 4096 символов текста) - если сценарий большой, лучше прикрепить файл:",
            reply_markup=keyboard
        )
        # Добавим информацию о балансе и лимитах
        await update.message.reply_text(
            f"{update.message.text}\n\n"
            f"Ваш текущий баланс: {balance} токенов\n"
            f"Лимит страниц на анализ: {self.PAGE_LIMIT}\n"
            f"Используйте /balance для проверки баланса и /limits для просмотра лимитов."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "🤖 <b>Как использовать бота:</b>\n\n"
            "1. Отправьте текст для быстрого анализа\n"
            "2. Используйте команды:\n"
            "   /start - начать работу\n"
            "   /help - показать эту справку\n"
            "   /balance - проверить текущий баланс токенов\n"
            "   /add_tokens - запросить пополнение баланса токенов\n"
            "   /limits - просмотреть текущие ограничения\n\n"
            "📄 <b>Поддерживаемые форматы файлов:</b>\n"
            "• TXT - текстовые файлы\n"
            "• DOC/DOCX - документы Word\n"
            "• PDF - документы PDF (без OCR)\n\n"
            "Обратите внимание на ограничения по количеству страниц и токенов.\n"
            "Запросы на пополнение баланса рассматриваются администратором."
        )
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.HTML
        )




    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        if not update.message or not update.message.text:
            return

        text = update.message.text
        chat_id = update.effective_chat.id
        
        logger.info(f"Received message from {chat_id}: {text}")
        
        # Обработка кнопок меню
        if text in ["Выбрать структуру", "Помощь", "Автоопределение структуры"]:
            logger.info(f"Processing menu button: {text}")
            await self.handle_button(update, context)
            return

        try:
            # Отправляем сообщение о начале обработки
            processing_message = await update.message.reply_text(
                "🔄 Анализирую текст... Это может занять некоторое время."
            )
            
            structure = context.user_data.get('selected_structure', "Auto-detect")
            logger.info(f"Processing text with structure: {structure}")
            
            await self.process_text(update, context, text, structure)
            await processing_message.delete()
                
        except Exception as e:
            error_message = f"❌ Произошла ошибка при обработке сообщения: {str(e)}"
            logger.error(f"Error in handle_message: {e}", exc_info=True)
            await update.message.reply_text(error_message)

    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на текстовые кнопки"""
        if not update.message:
            return
            
        text = update.message.text
        chat_id = update.effective_chat.id
        logger.info(f"Processing button press from {chat_id}: {text}")
        
        if text == "Выбрать структуру":
            await self.choose_structure(update, context)
        elif text == "Помощь":
            await self.help_command(update, context)
        elif text == "Автоопределение структуры":
            context.user_data['selected_structure'] = "Auto-detect"
            await update.message.reply_text(
                "✅ Выбрано автоопределение структуры.\n"
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
            '🔍 Выберите тип нарративной структуры:',
            reply_markup=reply_markup
        )

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик inline кнопок"""
        query = update.callback_query
        if not query:
            return

        logger.info(f"Received callback query: {query.data}")
        
        try:
            await query.answer()
            chat_id = update.effective_chat.id
            
            # Сохраняем выбранную структуру
            context.user_data['selected_structure'] = query.data
            
            # Обновляем сообщение с подтверждением выбора
            structure_name = StructureType.get_display_name(query.data)
            await query.edit_message_text(
                f"✅ Выбрана структура: {structure_name}\n\n"
                "Теперь отправьте текст или файл для анализа."
            )
            
            logger.info(f"Structure selected for chat {chat_id}: {query.data}")
            
        except Exception as e:
            logger.error(f"Error in button handler: {e}", exc_info=True)
            await query.edit_message_text(
                "❌ Произошла ошибка при выборе структуры. Попробуйте еще раз."
            )

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик файлов"""
        if not update.message or not update.message.document:
            return
            
        try:
            file = await update.message.document.get_file()
            file_name = update.message.document.file_name
            file_extension = Path(file_name).suffix.lower()
            
            logger.info(f"Processing file: {file_name}")

            # Проверяем поддерживаемые форматы
            supported_extensions = {'.txt', '.doc', '.docx', '.pdf'}
            if file_extension not in supported_extensions:
                await update.message.reply_text(
                    "❌ Поддерживаются только следующие форматы:\n"
                    "• TXT - текстовые файлы\n"
                    "• DOC/DOCX - документы Word\n"
                    "• PDF - документы PDF"
                )
                return

            processing_message = await update.message.reply_text(
                f"🔄 Обрабатываю файл {file_name}..."
            )

            # Создаем временную директорию для работы с файлом
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file = Path(temp_dir) / file_name
                await file.download_to_drive(str(temp_file))
                
                text = None
                
                try:
                    # Извлекаем текст в зависимости от формата файла
                    if file_extension == '.txt':
                        with open(temp_file, 'r', encoding='utf-8') as f:
                            text = f.read()
                            
                    elif file_extension in ['.doc', '.docx']:
                        text = extract_doc_text(temp_file)
                            
                    elif file_extension == '.pdf':
                        text = extract_text_from_pdf(temp_file)

                except FileNotFoundError:
                    await processing_message.edit_text(
                        "❌ Ошибка: файл не найден или недоступен."
                    )
                    return
                except ValueError as e:
                    await processing_message.edit_text(
                        f"❌ Ошибка: {str(e)}"
                    )
                    return
                except Exception as e:
                    logger.error(f"Error processing file {file_name}: {str(e)}")
                    await processing_message.edit_text(
                        "❌ Ошибка при обработке файла. "
                        "Возможно, файл поврежден или имеет неподдерживаемый формат."
                    )
                    return

            if not text or not text.strip():
                await processing_message.edit_text(
                    "❌ Не удалось извлечь текст из файла. "
                    "Возможно, файл пуст или содержит только изображения."
                )
                return

            # Проверка длины текста и предупреждение пользователя
            if len(text) > 50000:  # примерное ограничение
                await update.message.reply_text(
                    "⚠️ Внимание: текст очень длинный. "
                    "Анализ может занять продолжительное время."
                )

            structure = context.user_data.get('selected_structure', "Auto-detect")
            await self.process_text(update, context, text, structure)
            await processing_message.delete()
            
        except Exception as e:
            logger.error(f"Error in handle_document: {e}", exc_info=True)
            await update.message.reply_text(
                "❌ Произошла ошибка при обработке файла. "
                "Пожалуйста, убедитесь, что файл не поврежден и попробуйте снова."
            )
    
    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        try:
            user_data = self.db.get_user_data(user_id)
            if user_data is None or "token_balance" not in user_data:
                # Если данных пользователя нет или нет информации о балансе,
                # устанавливаем значение по умолчанию
                balance = self.DEFAULT_TOKEN_BALANCE
                self.db.update_user_balance(user_id, balance)
            else:
                balance = user_data["token_balance"]
            
            await update.message.reply_text(
                f"Ваш текущий баланс: {balance} токенов.",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error in balance_command for user {user_id}: {e}", exc_info=True)
            await update.message.reply_text(
                "Произошла ошибка при получении баланса. Пожалуйста, попробуйте позже или обратитесь к администратору.",
                parse_mode=ParseMode.HTML
            )


    async def limits_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f"Текущие лимиты:\n"
            f"- Максимальное количество страниц на анализ: {self.PAGE_LIMIT}\n"
            f"- Примерное количество токенов на страницу: {self.TOKENS_PER_PAGE}\n"
            f"- Максимальное количество токенов на анализ: {self.PAGE_LIMIT * self.TOKENS_PER_PAGE}"
        )

    async def add_tokens_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        try:
            amount = int(context.args[0])
            if amount <= 0:
                raise ValueError("Количество токенов должно быть положительным числом")
            
            await context.bot.send_message(
                chat_id=self.admin_id,
                text=f"Пользователь {user.first_name} (ID: {user.id}) запросил пополнение баланса на {amount} токенов.\n"
                     f"Для подтверждения используйте команду:\n"
                     f"/approve_tokens {user.id} {amount}"
            )
            
            await update.message.reply_text("Ваш запрос на пополнение баланса отправлен администратору. Пожалуйста, ожидайте подтверждения.")
        except (IndexError, ValueError):
            await update.message.reply_text("Пожалуйста, укажите корректное количество токенов для пополнения. Например: /add_tokens 1000")

    async def approve_tokens_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user_id = int(context.args[0])
            amount = int(context.args[1])
            new_balance = self.balance_service.add_tokens(user_id, amount)
            
            await context.bot.send_message(
                chat_id=user_id,
                text=f"Ваш запрос на пополнение баланса одобрен. Добавлено {amount} токенов. Новый баланс: {new_balance} токенов."
            )
            
            await update.message.reply_text(f"Баланс пользователя (ID: {user_id}) успешно пополнен на {amount} токенов. Новый баланс: {new_balance}")
        except (IndexError, ValueError):
            await update.message.reply_text("Пожалуйста, используйте команду в формате: /approve_tokens <user_id> <amount>")

    async def process_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, structure: str):
        """Обработка текста и отправка результатов анализа"""
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        user_data = self.db.get_user_data(user_id)
        user_balance = user_data.get("token_balance", 0)
        logger.info(f"Processing text for chat {chat_id} with structure {structure}")
        
        # Проверяем наличие баланса токенов в данных пользователя
        if "token_balance" not in user_data:
            # Если баланса нет, устанавливаем значение по умолчанию
            user_data["token_balance"] = self.DEFAULT_TOKEN_BALANCE
            self.db.update_user_balance(user_id, self.DEFAULT_TOKEN_BALANCE)
        
        # Проверяем баланс токенов
        if user_data["token_balance"] <= 0:
            await update.message.reply_text("У вас недостаточно токенов для анализа. Пожалуйста, обратитесь к администратору для пополнения баланса.")
            return

        # Оцениваем количество страниц и токенов
        estimated_pages = len(text) // 1000  # Примерно 1000 символов на страницу
        estimated_tokens = estimated_pages * self.TOKENS_PER_PAGE

        if estimated_pages > self.PAGE_LIMIT:
            await update.message.reply_text(f"Текст превышает установленный лимит в {self.PAGE_LIMIT} страниц. Текущий размер: примерно {estimated_pages} страниц.")
            return

        if estimated_tokens > user_data["token_balance"]:
            await update.message.reply_text(f"Недостаточно токенов для анализа. Требуется примерно {estimated_tokens} токенов, а у вас {user_data['token_balance']}.")
            return
        
        try:
            if structure == "Auto-detect":
                logger.info("Using auto-detection for structure")
                try:
                    structure = self.evaluator.classify(text)
                    logger.info(f"Auto-detected structure: {structure}")
                except Exception as e:
                    logger.error(f"Error in structure classification: {e}")
                    await update.message.reply_text(
                        "❌ Ошибка при определении структуры. Попробуйте выбрать структуру вручную."
                    )
                    return

            result = self.evaluator.analyze_specific_structure(text, structure)

            # Перед анализом считаем токены
            tokens_used = result['tokens_used']
        
            if tokens_used > user_balance:
                await update.message.reply_text(f"Недостаточно токенов. Требуется: {tokens_used}, доступно: {user_balance}")
                return

            new_balance = user_balance - tokens_used
            self.db.update_user_balance(user_id, new_balance)
            
            # Проверяем наличие и тип результата
            if not isinstance(result, dict):
                raise ValueError("Invalid result format")
            
            # Формируем упрощенный ответ без визуализации
            response_parts = []
            
            # Добавляем информацию о структуре
            if 'structure' in result:
                response_parts.append(f"📊 <b>Тип структуры:</b> {result['structure']}\n")
            
            # Добавляем основной анализ
            if 'analysis' in result and result['analysis']:
                analysis_text = str(result['analysis']).replace('*', '•')
                response_parts.append(f"<b>Анализ текста:</b>\n{analysis_text}")
            
            # Объединяем все части
            response = '\n'.join(response_parts)
            
            # Добавляем информацию о токенах
            response += f"\n\nИспользовано токенов: {tokens_used}\n"
            response += f"Оставшийся баланс: {new_balance} токенов"

            # Разбиваем длинные сообщения на части если необходимо
            if len(response) > 4096:
                for x in range(0, len(response), 4096):
                    await update.message.reply_text(
                        response[x:x+4096],
                        parse_mode=ParseMode.HTML
                    )
            else:
                await update.message.reply_text(
                    response,
                    parse_mode=ParseMode.HTML
                )
                    
        except Exception as e:
            logger.error(f"Error in process_text: {e}", exc_info=True)
            await update.message.reply_text(
                "❌ Произошла ошибка при анализе текста. Пожалуйста, попробуйте позже."
            )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"Exception while handling an update: {context.error}", exc_info=True)
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."
            )
