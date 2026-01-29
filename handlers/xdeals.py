from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from services.products import get_products_by_category, get_product_by_code
from services.tickets import create_ticket

def xdeals_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Streaming", callback_data="xdeals:cat:STREAMING")],
        [InlineKeyboardButton("🤖 Inteligência Artificial", callback_data="xdeals:cat:AI")],
        [InlineKeyboardButton("📡 IPTV", callback_data="xdeals:cat:IPTV")]
    ])

def xdeals_category(category):
    products = get_products_by_category(category)

    keyboard = [
        [InlineKeyboardButton(
            f"{p['name']} — R${p['price']}",
            callback_data=f"xdeals:prod:{p['code']}"
        )]
        for p in products
    ]

    keyboard.append([InlineKeyboardButton("⬅️ Voltar", callback_data="xdeals")])
    return InlineKeyboardMarkup(keyboard)

def handle_xdeals_product(user, product_code):
    product = get_product_by_code(product_code)
    ticket = create_ticket(user["id"], product)

    text = (
        f"🧾 *Ticket criado*\n\n"
        f"📦 {product['name']}\n"
        f"💰 R${product['price']}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Pagar agora", callback_data=f"pay:{ticket['id']}")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="xdeals")]
    ])

    return text, keyboard
