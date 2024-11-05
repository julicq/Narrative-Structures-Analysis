from db.database import Database

class BalanceService:
    def __init__(self):
        self.db = Database()

    def add_tokens(self, user_id: int, amount: int) -> int:
        user_data = self.db.get_user_data(user_id)
        new_balance = user_data["token_balance"] + amount
        self.db.update_user_balance(user_id, new_balance)
        return new_balance

    def get_balance(self, user_id: int) -> int:
        user_data = self.db.get_user_data(user_id)
        return user_data["token_balance"]