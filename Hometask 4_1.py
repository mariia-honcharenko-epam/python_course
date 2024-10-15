import random
import string

# Крок 1: Генерація випадкового списку словників
def generate_random_dictionaries():
    num_dicts = random.randint(2, 10)  # Випадкова кількість словників (від 2 до 10)
    list_of_dicts = []
    for d in range(num_dicts):
        num_keys = random.randint(1, 5)  # Випадкова кількість ключів у кожному словнику
        random_dict = {random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in range(num_keys)}
        list_of_dicts.append(random_dict)
    return list_of_dicts

random_dictionaries = generate_random_dictionaries()
print("Випадкові словники:", random_dictionaries)

# Крок 2: Об'єднання словників в один з урахуванням заданих умов
def merge_dictionaries(dicts):
    merged_dict = {}
    # Відслідковує максимальне значення та індекс словника для кожного ключа
    key_source = {}
    for index, d in enumerate(dicts):
        for key, value in d.items():
            if key not in merged_dict or value > merged_dict[key]:
                merged_dict[key] = value
                key_source[key] = index + 1  # Запам'ятовуємо індекс словника з максимальним значенням для цього ключа

    # Створення фінального словника з перейменованими ключами за необхідності
    final_dict = {}
    for key, value in merged_dict.items():
        if list(key_source.keys()).count(key) > 1:
            new_key = f"{key}_{key_source[key]}"
        else:
            new_key = key
        final_dict[new_key] = value
    return final_dict

# Об'єднання словників за правилами та вивід результату
combined_dictionary = merge_dictionaries(random_dictionaries)
print("Об'єднаний словник:", combined_dictionary)
