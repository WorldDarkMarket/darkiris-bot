import requests
import os

MISTICPAY_KEY = os.getenv("MISTICPAY_API_KEY")

def create_payment(amount, description):
    payload = {
        "amount": amount,
        "currency": "BRL",
        "description": description
    }

    headers = {
        "Authorization": f"Bearer {MISTICPAY_KEY}"
    }

    return requests.post(
        "https://api.misticpay.com/v1/payments",
        json=payload,
        headers=headers
    ).json()
