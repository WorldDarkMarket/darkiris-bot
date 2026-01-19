# utils.py
import re

def normalize_text(text: str) -> str:
    return text.strip().lower()

def contains_keywords(text: str, keywords: list[str]) -> bool:
    text = normalize_text(text)
    return any(k in text for k in keywords)

def extract_amount(text: str):
    """
    Extrai valores monetários simples:
    ex: 'quero 50', 'valor 120.90'
    """
    match = re.search(r"(\d+([.,]\d+)?)", text)
    if match:
        return float(match.group(1).replace(",", "."))
    return None
