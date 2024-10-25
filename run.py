# run.py

from app import create_app
import threading
import telegram_bot

app = create_app()

if __name__ == '__main__':
    # Запуск Flask-приложения в отдельном потоке
    flask_thread = threading.Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False})
    flask_thread.start()

    # Запуск Telegram-бота
    telegram_bot.main()
