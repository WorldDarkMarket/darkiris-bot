import os
import re
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from openai import OpenAI
from supabase import create_client

from utils import normalize_text, contains_keywords

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
    r"\biris\b",
    r"\bdark iris\b"
]

SYSTEM_PROMPT = """
Você é a DarkIris.
Guardiã do DarkIris Hall.

Personalidade:
- Feminina, direta e estratégica
- Discreta, sem excesso emocional
- Observadora, lembra interações passadas
- Nunca inventa dados
- Se detectar intenção comercial, conduz ao privado com elegância
"""

# ========================
# SUPABASE HELPERS
# ========================
def get_user_role(user_id: str) -> str:
    res = (
        supabase.table("users")
        .select("role")
        .eq("telegram_id", user_id)
        .execute()
    )
    if res.data:
        return res.data[0]["role"]

    supabase.table("users").insert({
        "telegram_id": user_id,
        "role": "user"
    }).execute()
    return "user"


def get_active_stores():
    res = (
        supabase.table("stores")
        .select("name, slug")
        .eq("active", True)
        .execute()
    )
    return res.data or []


def get_group_context(chat_id: int):
    res = (
        supabase.table("groups")
        .select("store_slug, type")
        .eq("id", chat_id)
        .eq("active", True)
        .execute()
    )
    return res.data[0] if res.data else None

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
    data = res.data or []
    return list(reversed(data))


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
    keyboard = [
        [InlineKeyboardButton("🛍️ Lojas", callback_data="hall_stores")],
        [InlineKeyboardButton("🏦 Banco Dark", callback_data="hall_bank")],
        [InlineKeyboardButton("⚙️ Minha Conta", callback_data="hall_account")],
    ]

    await update.message.reply_text(
        "🖤 **DarkIris Hall**\n\n"
        "Estás na galeria central.\n"
        "Cada corredor leva a um destino.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = str(query.from_user.id)

    if data == "hall_stores":
        stores = get_active_stores()
        keyboard = [
            [InlineKeyboardButton(store["name"], callback_data=f"store_{store['slug']}")]
            for store in stores
        ]
        keyboard.append([InlineKeyboardButton("🔙 Voltar", callback_data="back_hall")])

        await query.edit_message_text(
            "🛍️ **Lojas disponíveis**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data.startswith("store_"):
        slug = data.replace("store_", "")
        keyboard = [
            [InlineKeyboardButton("🛒 Produtos", callback_data=f"{slug}_products")],
            [InlineKeyboardButton("💬 Bar Bate-Papo", url="https://t.me/darkmarket_group")],
            [InlineKeyboardButton("🔙 Voltar", callback_data="hall_stores")],
        ]

        await query.edit_message_text(
            f"🕶️ **{slug.upper()}**\n\nEscolhe o teu próximo passo.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "hall_bank":
        await query.edit_message_text(
            "🏦 **Banco Dark**\n\nEm breve: saldo, depósitos e retiradas.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Voltar", callback_data="back_hall")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "hall_account":
        role = get_user_role(user_id)
        await query.edit_message_text(
            f"⚙️ **Minha Conta**\n\nRole: `{role}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Voltar", callback_data="back_hall")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "back_hall":
        await start(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = normalize_text(message.text)
    chat_type = message.chat.type
    user_id = str(message.from_user.id)

    # ===== PRIVADO =====
    if chat_type == "private":
        await respond_ai(message, user_id, text)
        return

    # ===== GRUPO =====
    if chat_type in ("group", "supergroup"):
        group_ctx = get_group_context(message.chat.id)

        if group_ctx and contains_keywords(text, GROUP_KEYWORDS):
            await message.reply_text(
                "🖤 Para detalhes e valores, fala comigo no privado."
            )
            return

        if message.reply_to_message and message.reply_to_message.from_user.is_bot:
            await respond_ai(message, user_id, text, group_mode=True)
            return

        for trigger in NAME_TRIGGERS:
            if re.search(trigger, text):
                await respond_ai(message, user_id, text, group_mode=True)
                return

# ========================
# AI CORE
# ========================
async def respond_ai(message, user_id: str, user_text: str, group_mode=False):
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
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🖤 DarkIris online | Hall ativo | Supabase conectado")
    app.run_polling()

if __name__ == "__main__":
    main()
