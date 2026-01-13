import os
import sys
import subprocess

# 🔧 Auto-instala dependências se não existirem
try:
    from telegram import Update
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==21.6", "requests"])
    from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import requests

# =========================
# ENV VARS
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN não definido")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY não definido")

# =========================
# HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🖤 Eu sou a DarkIris.\nFala comigo normalmente."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://darkiris.bot",
        "X-Title": "DarkIrisBot"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Você é a DarkIris, uma IA feminina, direta, inteligente e segura."
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "⚠️ Algo correu mal. Tenta novamente."

    await update.message.reply_text(reply)

# =========================
# MAIN
# =========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 DarkIris está online...")
    app.run_polling()

if __name__ == "__main__":
    main()
