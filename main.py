import os
import re
from datetime import datetime

from telegram import Update, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)

from openai import OpenAI
from supabase import create_client

from menus import hall_menu, lojas_menu, em_breve_menu
from utils import normalize_text, contains_keywords

# ========================
# ENV
# ========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

HALL_IMAGE_FILE_ID = os.getenv("HALL_IMAGE_FILE_ID")  # <- coloca no Render

# ========================
# CLIENTS
# ========================
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========================
# CONFIG
# ========================
GROUP_KEYWORDS = [
    "preço", "valor", "stock", "estoque",
    "como funciona", "informação", "info",
    "ajuda", "suporte"
]

NAME_TRIGGERS = [
    r"\bdarkiris\b",
    r"\biris\b",
    r"\bdark iris\b"
]

SYSTEM_PROMPT = """
Você é a DarkIris.

Guardião do DarkIris Hall.
Elegante, estratégica e observadora.

Nunca explica a estrutura interna.
Nunca inventa dados.
Reconhece autoridade do Boss.
Conduz assuntos comerciais ao privado.
"""

# ========================
# MEMORY
# ========================
def load_memory(user_id: str, limit: int = 10):
    res = (
        supabase.table("darkiris_memory")
        .select("role, content")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return list(reversed(res.data or []))

def save_memory(user_id: str, role: str, content: str):
    supabase.table("darkiris_memory").insert({
        "user_id": user_id,
        "role": role,
        "content": content,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

# ========================
# START
# ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if HALL_IMAGE_FILE_ID:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=HALL_IMAGE_FILE_ID
        )

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "🖤 **Bem-vindo ao DarkIris Hall**\n\n"
            "Os corredores estão abertos.\n"
            "Explora com liberdade.\n\n"
            "Eu observo. Intervenho quando necessário."
        ),
        reply_markup=hall_menu(),
        parse_mode="Markdown"
    )

# ========================
# CALLBACKS
# ========================
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "hall":
        await query.edit_message_text(
            text="🏛️ **DarkIris Hall**",
            reply_markup=hall_menu(),
            parse_mode="Markdown"
        )

    elif data == "hall_lojas":
        await query.edit_message_text(
            text=(
                "🛍️ **As tuas lojas preferidas**\n\n"
                "Desde oportunidades inteligentes na XDeals,\n"
                "serviços reservados na DarkMarket,\n"
                "até o universo tecnológico da AcademiaGhost."
            ),
            reply_markup=lojas_menu(),
            parse_mode="Markdown"
        )

    elif data == "hall_lazer":
        await query.edit_message_text(
            text=(
                "🎮 **Área de Lazer**\n\n"
                "Espaços exclusivos estão a ser preparados.\n"
                "Acabamentos finais em curso.\n\n"
                "Em breve."
            ),
            reply_markup=em_breve_menu(),
            parse_mode="Markdown"
        )

    elif data.startswith("loja_"):
        await query.edit_message_text(
            text="🚧 Esta loja está a ser organizada.\nVolta em breve.",
            reply_markup=em_breve_menu()
        )

# ========================
# AI CHAT
# ========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = normalize_text(message.text)
    chat_type = message.chat.type
    user_id = str(message.from_user.id)

    if chat_type == "private":
        await respond_ai(message, user_id, text)
        return

    if chat_type in ("group", "supergroup"):
        if message.reply_to_message and message.reply_to_message.from_user.is_bot:
            await respond_ai(message, user_id, text, group_mode=True)
            return

        for trigger in NAME_TRIGGERS:
            if re.search(trigger, text):
                await respond_ai(message, user_id, text, group_mode=True)
                return

        if contains_keywords(text, GROUP_KEYWORDS):
            await respond_ai(message, user_id, text, group_mode=True)
            return

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

    reply = response.choices[0].message.content.strip()

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
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🖤 DarkIris Hall online.")
    app.run_polling()

if __name__ == "__main__":
    main()
