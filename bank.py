from services.bank_ledger import get_balance

def get_wallet(user_id):
    return {
        "balance": get_balance(user_id)
    }

def get_bank_settings():
    return {
        "currency": "BRL"
    }

def get_transactions(user_id):
    return []

