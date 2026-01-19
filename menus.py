from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🛍 XDeals", callback_data="store_xdeals")],
        [InlineKeyboardButton("🕶 DarkMarket", callback_data="store_darkmarket")],
        [InlineKeyboardButton("🎓 AcademiaGhost", callback_data="store_academia")]
    ]
    return InlineKeyboardMarkup(keyboard)

