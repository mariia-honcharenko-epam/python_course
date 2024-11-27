import re

def normalize_text(text):
    """Функція нормалізує текст так, що кожне речення починається з великої літери."""
    text = text.lower()
    return re.sub(r'(?<!\w)[a-zA-Z]', lambda x: x.group(0).upper(), text)