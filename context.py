def detect_store_from_chat(chat_title):
    if not chat_title:
        return None
    title = chat_title.lower()
    if "xdeal" in title:
        return "xdeals"
    if "dark" in title:
        return "darkmarket"
    if "ghost" in title:
        return "academiaghost"
    return None
