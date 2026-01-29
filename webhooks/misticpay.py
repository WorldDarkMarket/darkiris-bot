import os
import hmac
import hashlib
from fastapi import Request, HTTPException

from services.bank_ledger import create_transaction
from services.tickets import mark_ticket_paid
from services.delivery import deliver_service
from data.xdeals_products import XDEALS_PRODUCTS

MISTICPAY_WEBHOOK_SECRET = os.getenv("MISTICPAY_WEBHOOK_SECRET")

def verify_signature(payload: bytes, signature: str):
    expected = hmac.new(
        MISTICPAY_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


async def handle_misticpay_webhook(request: Request, bot):
    raw_body = await request.body()
    signature = request.headers.get("X-MisticPay-Signature")

    if not signature or not verify_signature(raw_body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()

    event = payload.get("event")
    data = payload.get("data")

    if event != "payment.completed":
        return {"status": "ignored"}

    ticket_id = data["reference"]
    amount = float(data["amount"])
    tx_id = data["id"]

    # 1️⃣ marcar ticket pago
    mark_ticket_paid(ticket_id)

    # 2️⃣ ledger
    create_transaction(
        user_id=None,  # será ligado via ticket futuramente
        tx_type="payment",
        amount=-amount,
        currency=data.get("currency", "BRL"),
        reference=tx_id
    )

    # 3️⃣ entrega automática (temporária)
    deliver_service(
        bot=bot,
        chat_id=int(ticket_id.split("_")[1]),  # simplificado nesta fase
        product=XDEALS_PRODUCTS[0]
    )

    return {"status": "ok"}
