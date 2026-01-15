import os
import re
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# ========================
# ENV
# ========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

# ========================
# OpenRouter Client
# ========================
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ========================
# Configuração DarkIris
# ========================
GROUP_KEYWORDS = [
    "preço", "valor", "stock", "estoque",
    "como funciona", "informação", "info",
    "ajuda", "suporte"
]

NAME_TRIGGERS = [
    r"\bdarkiris\b",
    r"\biris\b"
]

SYSTEM_PROMPT = """
Você é a DarkIris.
Uma IA feminina, direta, inteligente e discreta.

Regras:
- Seja clara e objetiva.
- Nunca seja excessivamente simpática.
- Não invente informações.
- Se detectar interesse comercial, convide educadamente para falar no privado.
"""

# ========================
# Handlers
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🖤 Eu sou a DarkIris.\nPodes falar comigo normalmente."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()
    chat_type = message.chat.type

    # ===== PRIVADO =====
    if chat_type == "private":
        await respond_ai(message, text)
        return

    # ===== GRUPO =====
    if chat_type in ["group", "supergroup"]:

        # 1. Reply direto a mensagem da bot
        if message.reply_to_message and message.reply_to_message.from_user.is_bot:
            await respond_ai(message, text, group_mode=True)
            return

        # 2. Nome da bot no texto (DarkIris / Iris)
        for trigger in NAME_TRIGGERS:
            if re.search(trigger, text):
                await respond_ai(message, text, group_mode=True)
                return

        # 3. Palavra-chave comercial
        if any(keyword in text for keyword in GROUP_KEYWORDS):
            await respond_ai(message, text, group_mode=True)
            return

async def respond_ai(message, user_text, group_mode=False):
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0.6,
        max_tokens=250
    )

    reply = response.choices[0].message.content

    if group_mode:
        reply += "\n\n🖤 Podemos falar melhor no privado."

    await message.reply_text(reply)

# ========================
# Main
# ========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 DarkIris está online e atenta.")
    app.run_polling()

if __name__ == "__main__":
    main()
