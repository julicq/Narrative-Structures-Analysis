# db/database.py

import sqlite3
from typing import Dict, Any
import os

class Database:
    def __init__(self, db_name: str = 'db/user_data.db'):
        db_exists = os.path.exists(db_name)
        self.conn = sqlite3.connect(db_name)
        if not db_exists:
            self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    token_balance INTEGER NOT NULL DEFAULT 0
                )
            ''')

    def get_user_data(self, user_id: int) -> Dict[str, Any]:
        with self.conn:
            cursor = self.conn.execute('SELECT token_balance FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if result:
                return {"token_balance": result[0]}
            else:
                return {"token_balance": 0}

    def update_user_balance(self, user_id: int, new_balance: int):
        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO users (user_id, token_balance)
                VALUES (?, ?)
            ''', (user_id, new_balance))

    def close(self):
        self.conn.close()
