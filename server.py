from fastapi import FastAPI, Request
from .webhooks.mistic import handle_misticpay_webhook

app = FastAPI()

@app.post("/webhooks/misticpay")
async def misticpay_webhook(request: Request):
    # bot ainda None nesta fase (ok)
    return await handle_misticpay_webhook(request, bot=None)

