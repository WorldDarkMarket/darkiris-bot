import os
import re
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from openai import OpenAI
from supabase import create_client

# ========================
# ENV
# ========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# ========================
# CLIENTS
# ========================
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========================
# CONFIG DarkIris
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
Uma IA feminina, direta, inteligente e estratégica.

Personalidade:
- Discreta, firme, sem excesso emocional
- Observadora, lembra interações passadas
- Não inventa dados
- Se houver intenção comercial, conduz ao privado com elegância
"""

# ========================
# MEMORY FUNCTIONS
# ========================
def load_memory(user_id: str, limit: int = 10):
    data = (
        supabase.table("darkiris_memory")
        .select("role, content")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data
    )
    return list(reversed(data)) if data else []

def save_memory(user_id: str, role: str, content: str):
    supabase.table("darkiris_memory").insert({
        "user_id": user_id,
        "role": role,
        "content": content,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

# ========================
# HANDLERS
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🖤 Eu sou a DarkIris.\nFala comigo."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.strip()
    chat_type = message.chat.type
    user_id = str(message.from_user.id)

    if chat_type == "private":
        await respond_ai(message, user_id, text)
        return

    if chat_type in ["group", "supergroup"]:
        if message.reply_to_message and message.reply_to_message.from_user.is_bot:
            await respond_ai(message, user_id, text, group_mode=True)
            return

        for trigger in NAME_TRIGGERS:
            if re.search(trigger, text.lower()):
                await respond_ai(message, user_id, text, group_mode=True)
                return

        if any(keyword in text.lower() for keyword in GROUP_KEYWORDS):
            await respond_ai(message, user_id, text, group_mode=True)
            return

# ========================
# AI CORE
# ========================
async def respond_ai(message, user_id, user_text, group_mode=False):
    history = load_memory(user_id)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=messages,
        temperature=0.6,
        max_tokens=300
    )

    reply = response.choices[0].message.content

    save_memory(user_id, "user", user_text)
    save_memory(user_id, "assistant", reply)

    if group_mode:
        reply += "\n\n🖤 No privado consigo orientar melhor."

    await message.reply_text(reply)

# ========================
# MAIN
# ========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🖤 DarkIris online. Memória ativa.")
    app.run_polling()

if __name__ == "__main__":
    main()
