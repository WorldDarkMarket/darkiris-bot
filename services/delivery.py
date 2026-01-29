from telegram import Bot

def deliver_service(bot: Bot, chat_id: int, product):
    message = (
        f"✅ *Entrega concluída*\n\n"
        f"📦 {product['name']}\n\n"
        "🔐 Os dados serão enviados abaixo."
    )

    bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode="Markdown"
    )

    # 👉 aqui futuramente:
    # - enviar ficheiro
    # - enviar markdown
    # - consumir stock
