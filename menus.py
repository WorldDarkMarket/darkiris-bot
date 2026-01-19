from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🛒 Loja", callback_data="menu_shop")],
        [InlineKeyboardButton("💳 Recarregar saldo", callback_data="menu_topup")],
        [InlineKeyboardButton("📦 Meus pedidos", callback_data="menu_orders")],
        [InlineKeyboardButton("🆘 Suporte", callback_data="menu_support")]
    ]
    return InlineKeyboardMarkup(keyboard)
