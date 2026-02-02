from fastapi import Request
from services.bank_ledger import create_transaction
from services.tickets import mark_ticket_paid
from services.delivery import deliver_service
from data.xdeals_products import XDEALS_PRODUCTS


async def handle_misticpay_webhook(request: Request, bot):
    payload = await request.json()

    # MisticPay envia status da transação
    status = payload.get("status")
    tx_id = payload.get("transactionId")
    amount = float(payload.get("value", 0))
    reference = payload.get("reference")

    # só processa quando pagamento estiver concluído
    if status not in ["PAID", "COMPLETED", "CONFIRMED"]:
        return {"status": "ignored"}

    # 1️⃣ marcar ticket como pago
    mark_ticket_paid(reference)

    # 2️⃣ ledger
    create_transaction(
        user_id=None,
        tx_type="payment",
        amount=-amount,
        currency="BRL",
        reference=tx_id
    )

    # 3️⃣ entrega automática
    deliver_service(
        bot=bot,
        chat_id=int(reference.split("_")[1]),
        product=XDEALS_PRODUCTS[0]
    )

    return {"status": "ok"}

