import re

text = """
homEwork:
tHis iz your homeWork, copy these Text to variable.



You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.

"""

# 1: Нормалізація тексту до нижнього регістру
normalized_text = text.lower()

# 2: Виправлення конкретних помилок написання 'iz' на 'is'
corrected_text = re.sub(r'\biz\b', 'is', normalized_text)

# 3: Витягуємо останнє слово з кожного речення і формуємо нове речення
sentences = corrected_text.split('.')
last_words = [sentence.strip().split()[-1] if sentence.strip() else '' for sentence in sentences]
new_sentence = ' '.join(last_words)

# Додаємо нове речення до існуючого тексту
updated_paragraph = corrected_text.strip() + ' ' + new_sentence + '.'

# 4: Рахуємо всі пробільні символи
whitespace_count = len(re.findall(r'\s', corrected_text))

print("Нормалізований та виправлений текст:\n")
print(updated_paragraph)
print("\nКількість пробільних символів:", whitespace_count)