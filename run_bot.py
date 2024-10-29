# run_bot.py

import asyncio
import logging
from bot.telegram_bot import TelegramBot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Основная функция запуска бота"""
    bot = TelegramBot()
    bot.run()

if __name__ == "__main__":
    main()
