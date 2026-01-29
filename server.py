from fastapi import FastAPI, Request
from webhooks.mistic import handle_misticpay_webhook
from telegram import Bot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)

app = FastAPI()

@app.post("/webhooks/misticpay")
async def misticpay_webhook(request: Request):
    return await handle_misticpay_webhook(request, bot)

