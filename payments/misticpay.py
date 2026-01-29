import requests
import os

MISTICPAY_API_KEY = os.getenv("MISTICPAY_API_KEY")
BASE_URL = "https://api.misticpay.com/v1"

def create_payment(amount, reference):
    payload = {
        "amount": amount,
        "currency": "BRL",
        "reference": reference
    }

    headers = {
        "Authorization": f"Bearer {MISTICPAY_API_KEY}"
    }

    # ⚠️ Simulado por enquanto
    return {
        "status": "paid",
        "tx_id": "SIMULATED_TX_123"
    }
