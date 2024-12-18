from db.database import Database
import logging

logger = logging.getLogger(__name__)

class BalanceService:
    def __init__(self):
        self.db = Database()

    def get_balance(self, user_id: int) -> int:
        """
        Получить текущий баланс пользователя
        
        Args:
            user_id: ID пользователя
            
        Returns:
            int: Текущий баланс
        """
        try:
            user_data = self.db.get_user_data(user_id)
            return user_data.get("token_balance", 0)
        except Exception as e:
            logger.error(f"Error getting balance for user {user_id}: {e}")
            return 0

    def add_tokens(self, user_id: int, amount: int) -> int:
        """
        Добавить токены к балансу пользователя
        
        Args:
            user_id: ID пользователя
            amount: Количество токенов для добавления
            
        Returns:
            int: Новый баланс
        """
        try:
            current_balance = self.get_balance(user_id)
            new_balance = current_balance + amount
            self.db.update_user_balance(user_id, new_balance)
            return new_balance
        except Exception as e:
            logger.error(f"Error adding tokens for user {user_id}: {e}")
            raise

    def use_tokens(self, user_id: int, amount: int) -> int:
        """
        Списать токены с баланса пользователя
        
        Args:
            user_id: ID пользователя
            amount: Количество токенов для списания
            
        Returns:
            int: Новый баланс
            
        Raises:
            ValueError: Если недостаточно токенов
        """
        try:
            current_balance = self.get_balance(user_id)
            if current_balance < amount:
                raise ValueError(f"Insufficient tokens. Required: {amount}, Available: {current_balance}")
            
            new_balance = current_balance - amount
            self.db.update_user_balance(user_id, new_balance)
            return new_balance
        except Exception as e:
            logger.error(f"Error using tokens for user {user_id}: {e}")
            raise
