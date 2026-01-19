from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def hall_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛍️ Lojas", callback_data="hall_lojas"),
            InlineKeyboardButton("🏦 Banco", callback_data="hall_banco")
        ],
        [
            InlineKeyboardButton("🎮 Lazer", callback_data="hall_lazer"),
            InlineKeyboardButton("💬 Bar Bate-Papo", url="https://t.me/darkiris_hall")
        ]
    ])

def lojas_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛍️ XDeals", callback_data="loja_xdeals"),
            InlineKeyboardButton("🕶️ DarkMarket", callback_data="loja_darkmarket")
        ],
        [
            InlineKeyboardButton("🧠 AcademiaGhost", callback_data="loja_academia")
        ],
        [
            InlineKeyboardButton("🏛️ Voltar ao Hall", callback_data="hall")
        ]
    ])

def em_breve_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏛️ Voltar ao Hall", callback_data="hall")
        ]
    ])
