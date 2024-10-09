import re


text = """
homEwork:
tHis iz your homeWork, copy these Text to variable.

You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

def normalize_text(text):
    """Нормалізує текст до нижнього регістру."""
    return text.lower()

def correct_mistakes(text):
    """Виправляє специфічні помилки в тексті."""
    return re.sub(r'\biz\b', 'is', text)

def extract_and_append_last_words(text):
    """Витягає останні слова з кожного речення та додає ці слова в кінці тексту як нове речення."""
    sentences = text.split('.')
    last_words = [sentence.strip().split()[-1] if sentence.strip() else '' for sentence in sentences]
    new_sentence = ' '.join(last_words)
    return text.strip() + ' ' + new_sentence + '.'

def count_whitespace_characters(text):
    """Рахує кількість пробільних символів у тексті."""
    return len(re.findall(r'\s', text))

# Обробка тексту за допомогою функцій
normalized_text = normalize_text(text)
corrected_text = correct_mistakes(normalized_text)
updated_paragraph = extract_and_append_last_words(corrected_text)
whitespace_count = count_whitespace_characters(corrected_text)

# Виводимо результат
print("Нормалізований та виправлений текст:\n")
print(updated_paragraph)
print("\nКількість пробільних символів:", whitespace_count)