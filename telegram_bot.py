import os
from dotenv import load_dotenv
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import os
from app.constants import STRUCTURE_MAPPING
from service.evaluator import NarrativeEvaluator
from service import initialize_llm
from app.routes import extract_doc_text, extract_text_from_pdf_miner, extract_text_from_txt

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация LLM и NarrativeEvaluator
llm = initialize_llm()
evaluator = NarrativeEvaluator(llm)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Я бот для анализа нарративных структур. Отправьте мне текст или файл (doc, docx, pdf, txt) для анализа.',
        reply_markup=get_main_keyboard()
    )

def get_main_keyboard():
    keyboard = [
        [KeyboardButton("Выбрать структуру"), KeyboardButton("Помощь")],
        [KeyboardButton("Автоопределение структуры")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Выбрать структуру":
        await choose_structure(update, context)
    elif text == "Помощь":
        await help_command(update, context)
    elif text == "Автоопределение структуры":
        context.user_data['selected_structure'] = "Auto-detect"
        await update.message.reply_text("Выбрано автоопределение структуры.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Вот что я умею:
    - Анализировать текст: просто отправьте мне текстовое сообщение
    - Анализировать файлы: отправьте мне файл (doc, docx, pdf, txt)
    - Выбирать тип структуры: используйте команду /choose_structure
    - Автоматически определять структуру: это происходит по умолчанию
    """
    await update.message.reply_text(help_text)

async def choose_structure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(structure, callback_data=structure)] for structure in STRUCTURE_MAPPING.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите тип нарративной структуры:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['selected_structure'] = query.data
    await query.edit_message_text(text=f"Выбрана структура: {query.data}")

async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    structure = context.user_data.get('selected_structure', "Auto-detect")
    await process_text(update, context, text, structure)

async def analyze_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    file_extension = os.path.splitext(file_name)[1].lower()

    if file_extension in ['.doc', '.docx']:
        await file.download_to_drive(file_name)
        text = extract_doc_text(file_name)
        os.remove(file_name)
    elif file_extension == '.pdf':
        await file.download_to_drive(file_name)
        with open(file_name, 'rb') as f:
            text = extract_text_from_pdf_miner(f)
        os.remove(file_name)
    elif file_extension == '.txt':
        await file.download_to_drive(file_name)
        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.read()
        os.remove(file_name)
    else:
        await update.message.reply_text("Неподдерживаемый тип файла. Пожалуйста, отправьте doc, docx, pdf или txt файл.")
        return

    structure = context.user_data.get('selected_structure', "Auto-detect")
    await process_text(update, context, text, structure)

async def process_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, structure: str):
    await update.message.reply_text("Анализирую текст...")

    if structure == "Auto-detect":
        structure = evaluator.classify(text)

    result = evaluator.analyze_specific_structure(text, structure)

    response = f"Анализ структуры: {result['structure']}\n\n"
    response += f"Анализ:\n{result['analysis']}\n\n"
    # response += f"Визуализация:\n{result['visualization']}"

    if len(response) > 4096:
        for x in range(0, len(response), 4096):
            await update.message.reply_text(response[x:x+4096])
    else:
        await update.message.reply_text(response)

def main():
    # Получение токена из переменных окружения
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("Не найден токен для Telegram бота. Убедитесь, что вы установили TELEGRAM_BOT_TOKEN в файле .env")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.Regex("^(Выбрать структуру|Помощь|Автоопределение структуры)$"), handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_text))
    app.add_handler(MessageHandler(filters.Document.ALL, analyze_file))

    app.run_polling()

if __name__ == '__main__':
    main()
