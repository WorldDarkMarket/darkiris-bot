import os
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from supabase import create_client
from openai import OpenAI

# ===== MENUS & ASSETS =====
from menus import hall_menu, lojas_menu, voltar_hall, bank_menu
from assets import (
    HALL_IMG, LOJAS_IMG,
    XDEALS_IMG, DARKMARKET_IMG,
    ACADEMIA_IMG, DARKLABS_IMG,
    BANK_IMG
)

# ===== SERVICES =====
from services.users import get_or_create_user
from services.tickets import create_ticket
from bank import get_wallet, get_bank_settings

# ===== DATA =====
from data.xdeals_products import XDEALS_PRODUCTS

# ===== PAYMENTS =====
from payments.misticpay import create_payment

# ================= ENV =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ================= CLIENTS =================
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

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
    tg_user = update.effective_user
    user_core = get_or_create_user(tg_user)

    context.user_data["persona"] = "iris"

    name = user_core.get("first_name") or "Visitante"

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

    get_or_create_user(query.from_user)
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
                "Aqui encontras as tuas lojas preferidas."
            ),
            reply_markup=lojas_menu(),
            parse_mode="Markdown"
        )

    # ===== XDEALS LISTA =====
    elif data == "xdeals":
        keyboard = [
            [
                InlineKeyboardButton(
                    f"{p['name']} — R${p['price']}",
                    callback_data=f"xdeal_buy:{p['code']}"
                )
            ]
            for p in XDEALS_PRODUCTS
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Voltar", callback_data="lojas")])

        await query.message.reply_text(
            "💸 **XDeals Brasil**\n\nSeleciona um serviço:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # ===== CRIAR TICKET =====
    elif data.startswith("xdeal_buy:"):
        code = data.split(":")[1]
        product = next(p for p in XDEALS_PRODUCTS if p["code"] == code)

        ticket = create_ticket(
            user_id=query.from_user.id,
            store_slug="xdeals",
            service_code=product["code"],
            title=product["name"],
            description=product.get("description"),
            payment_required=True
        )

        await query.message.reply_text(
            f"🧾 *Ticket criado*\n\n"
            f"📦 {product['name']}\n"
            f"💰 R${product['price']}\n\n"
            "Desejas pagar agora?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "💳 Pagar",
                    callback_data=f"pay_ticket:{ticket['id']}"
                )],
                [InlineKeyboardButton("❌ Cancelar", callback_data="hall")]
            ]),
            parse_mode="Markdown"
        )

    # ===== GERAR PAGAMENTO (NÃO CONFIRMA) =====
    elif data.startswith("pay_ticket:"):
        ticket_id = data.split(":")[1]

        payment = create_payment(
            reference=ticket_id
        )

        await query.message.reply_text(
            "💳 **Pagamento gerado**\n\n"
            "⏳ Aguardando confirmação automática.\n\n"
            f"🔗 {payment['payment_url']}",
            parse_mode="Markdown"
        )

    # ===== BANCO =====
    elif data == "banco":
        context.user_data["persona"] = "lucas"
        wallet = get_wallet(query.from_user.id)
        settings = get_bank_settings()

        await query.message.reply_photo(
            photo=BANK_IMG,
            caption=(
                "🏦 **Banco Central**\n\n"
                f"👤 ID: `{query.from_user.id}`\n"
                f"💰 Saldo: {wallet['balance']} {settings['currency']}"
            ),
            reply_markup=bank_menu(),
            parse_mode="Markdown"
        )

# ================= AI CHAT =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user
    get_or_create_user(tg_user)

    persona = context.user_data.get("persona", "iris")
    system_prompt = PROMPT_LUCAS if persona == "lucas" else PROMPT_IRIS

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": update.message.text}
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

    print("🖤 DarkIris Hall ONLINE | XDeals + Tickets + MisticPay READY")
    app.run_polling()

if __name__ == "__main__":
    main()



