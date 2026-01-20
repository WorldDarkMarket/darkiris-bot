import os
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

from supabase import create_client
from openai import OpenAI

from menus import hall_menu, lojas_menu, voltar_hall
from assets import (
    HALL_IMG, LOJAS_IMG,
    XDEALS_IMG, DARKMARKET_IMG,
    ACADEMIA_IMG, DARKLABS_IMG,
    BANK_IMG
)

from bank import get_wallet, get_bank_settings, get_transactions
from menus import bank_menu

# ================= ENV =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ================= CLIENTS =================
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

# ================= PERSONAS =================
PROMPT_IRIS = (
    "Você é DarkIris, guardiã elegante e estratégica do DarkIris Hall. "
    "Guia, observa e orienta. Nunca revela estrutura interna."
)

PROMPT_LUCAS = (
    "Você é Lucas, especialista bancário. Profissional, direto e objetivo. "
    "Lida apenas com assuntos financeiros."
)

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "Visitante"

    context.user_data["persona"] = "iris"

    text = (
        f"🖤 Olá novamente, {name}.\n\n"
        "Bem-vindo ao **DarkIris Hall**.\n"
        "Explora à vontade. Se precisares de algo, escreve — eu respondo."
    )

    await update.message.reply_photo(
        photo=HALL_IMG,
        caption=text,
        reply_markup=hall_menu(),
        parse_mode="Markdown"
    )

# ================= CALLBACKS =================
async def navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # ===== HALL =====
    if data == "hall":
        context.user_data["persona"] = "iris"
        await query.message.edit_caption(
            "🖤 Estás de volta ao **DarkIris Hall**.",
            reply_markup=hall_menu(),
            parse_mode="Markdown"
        )

    # ===== LOJAS =====
    elif data == "lojas":
        await query.message.reply_photo(
            photo=LOJAS_IMG,
            caption=(
                "🛍️ **Galeria Comercial**\n\n"
                "Aqui encontras as tuas lojas preferidas.\n"
                "Explora com calma."
            ),
            reply_markup=lojas_menu(),
            parse_mode="Markdown"
        )

    # ===== XDEALS =====
    elif data == "xdeals":
        await query.message.reply_photo(
            photo=XDEALS_IMG,
            caption=(
                "💸 **XDeals Brasil**\n\n"
                "Streaming, Viagens, Farmácia e Eventos.\n\n"
                "Canal oficial:\nhttps://t.me/+MV4U7W9fcqkxZjNh"
            ),
            reply_markup=voltar_hall(),
            parse_mode="Markdown"
        )

    # ===== DARKMARKET =====
    elif data == "darkmarket":
        await query.message.reply_photo(
            photo=DARKMARKET_IMG,
            caption=(
                "🕶️ **DarkMarket**\n\n"
                "Produtos e serviços conhecidos pelos membros.\n\n"
                "Grupo oficial:\n@DarkMarket_Group"
            ),
            reply_markup=voltar_hall(),
            parse_mode="Markdown"
        )

    # ===== ACADEMIA =====
    elif data == "academiaghost":
        await query.message.reply_photo(
            photo=ACADEMIA_IMG,
            caption=(
                "🎓 **AcademiaGhost**\n\n"
                "Formação, tecnologia e o DarkLab.\n\n"
                "Canal:\n@AcademiaGhost"
            ),
            reply_markup=voltar_hall(),
            parse_mode="Markdown"
        )

    # ===== DARKLABS =====
    elif data == "darklabs":
        await query.message.reply_photo(
            photo=DARKLABS_IMG,
            caption=(
                "🧪 **DarkLabs**\n\n"
                "Área restrita.\n"
                "Acessos sob aprovação."
            ),
            reply_markup=voltar_hall()
        )

    # ===== BANCO =====
elif data == "banco":
    context.user_data["persona"] = "lucas"

    wallet = get_wallet(query.from_user.id)
    settings = get_bank_settings()

    caption = (
        "🏦 **Banco Central**\n\n"
        f"👤 ID: `{query.from_user.id}`\n"
        f"💰 Saldo: {wallet['balance']} USDT\n\n"
        "Escolhe uma operação:"
    )

    await query.message.reply_photo(
        photo=BANK_IMG,
        caption=caption,
        reply_markup=bank_menu(),
        parse_mode="Markdown"
    )


# ================= AI CHAT =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    persona = context.user_data.get("persona", "iris")

    system_prompt = PROMPT_LUCAS if persona == "lucas" else PROMPT_IRIS

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.6,
        max_tokens=250
    )

    await update.message.reply_text(response.choices[0].message.content)

# ================= MAIN =================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(navigation))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🖤 DarkIris Hall ONLINE | Visual + Personas Ativas")
    app.run_polling()

if __name__ == "__main__":
    main()
