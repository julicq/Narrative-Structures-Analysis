# dashboard/routes.py

from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from service.llm import LLMFactory, ModelType, LLMManager
import sqlite3
from shared.config import Config
import os

dashboard = Blueprint('dashboard', __name__)
llm_manager = LLMManager()

def get_db_connection():
    conn = sqlite3.connect('db/user_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@dashboard.route('/')
def index():
    return render_template('dashboard/index.html')

@dashboard.route('/models', methods=['GET', 'POST'])
def manage_models():
    if request.method == 'POST':
        selected_models = [ModelType(model) for model in request.form.getlist('models')]
        Config.set_selected_models(selected_models)
        return redirect(url_for('dashboard.manage_models'))
    
    all_models = {model_type.value: model_name for model_type, model_name in LLMFactory.DEFAULT_MODELS.items()}
    selected_models = Config.get_selected_models()
    return render_template('dashboard/models.html', models=all_models, selected_models=selected_models)

@dashboard.route('/bot-messages', methods=['GET', 'POST'])
def manage_bot_messages():
    if request.method == 'POST':
        welcome_message = request.form.get('welcome')
        goodbye_message = request.form.get('goodbye')
        Config.set_bot_message('welcome', welcome_message)
        Config.set_bot_message('goodbye', goodbye_message)
        return redirect(url_for('dashboard.manage_bot_messages'))
    
    welcome_message = Config.get_bot_message('welcome')
    goodbye_message = Config.get_bot_message('goodbye')
    return render_template('dashboard/bot_messages.html', welcome_message=welcome_message, goodbye_message=goodbye_message)

@dashboard.route('/users')
def list_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('dashboard/users.html', users=users)