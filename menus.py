from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================
# HALL PRINCIPAL
# =========================
def hall_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛍️ Lojas", callback_data="lojas"),
            InlineKeyboardButton("🏦 Banco", callback_data="banco"),
        ],
        [
            InlineKeyboardButton("🎮 Lazer", callback_data="lazer"),
            InlineKeyboardButton("🧪 DarkLabs 🔒", callback_data="darklabs"),
        ],
        [
            InlineKeyboardButton("🍸 IrisBar Bate-Papo", url="https://t.me/DarkIrisHall"),
        ]
    ])


# =========================
# MENU DE LOJAS
# =========================
def lojas_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💸 XDeals Brasil", callback_data="store:xdeals")],
        [InlineKeyboardButton("🕶️ DarkMarket", callback_data="store:darkmarket")],
        [InlineKeyboardButton("🎓 AcademiaGhost", callback_data="store:academiaghost")],
        [
            InlineKeyboardButton("⬅️ Voltar ao Hall", callback_data="hall")
        ]
    ])


# =========================
# MENU DARKMARKET (categorias)
# =========================
def darkmarket_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 Logins", callback_data="cat:logins")],
        [InlineKeyboardButton("💳 Dark CC", callback_data="cat:dark-cc")],
        [InlineKeyboardButton("🎮 Dark GG", callback_data="cat:dark-gg")],
        [InlineKeyboardButton("🛠️ Serviços Especiais", callback_data="cat:services")],
        [
            InlineKeyboardButton("⬅️ Voltar às Lojas", callback_data="lojas"),
            InlineKeyboardButton("🏛️ Hall", callback_data="hall"),
        ]
    ])


# =========================
# MENU LAZER
# =========================
def lazer_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 Casino (em breve)", callback_data="coming_soon")],
        [InlineKeyboardButton("❌ Sala X (em breve)", callback_data="coming_soon")],
        [InlineKeyboardButton("🎲 Outros (em breve)", callback_data="coming_soon")],
        [
            InlineKeyboardButton("⬅️ Hall", callback_data="hall")
        ]
    ])


# =========================
# BOTÃO DARK BANK
# =========================
def bank_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Ver Saldo", callback_data="bank_balance")],
        [InlineKeyboardButton("➕ Depositar", callback_data="bank_deposit")],
        [InlineKeyboardButton("🔄 Converter", callback_data="bank_convert")],
        [InlineKeyboardButton("➖ Retirar", callback_data="bank_withdraw")],
        [InlineKeyboardButton("📜 Histórico", callback_data="bank_history")],
        [InlineKeyboardButton("⬅️ Voltar ao Hall", callback_data="hall")]
    ])


# =========================
# BOTÃO PADRÃO DE RETORNO
# =========================
def voltar_hall():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Voltar ao Hall", callback_data="hall")]
    ])

