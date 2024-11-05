from datetime import datetime, timedelta
import csv
import string
from collections import Counter


class News:
    def __init__(self, text, city):
        self.text = text
        self.city = city
        self.publish_date = datetime.now()

    def publish(self):
        return f"News ---------------\n{self.text}\n{self.city}, {self.publish_date.strftime('%d/%m/%Y %H:%M')}\n"


class PrivateAd:
    def __init__(self, text, expiration_date):
        self.text = text
        self.expiration_date = expiration_date

    def days_left(self):
        differ = self.expiration_date - datetime.now()
        return differ.days

    def publish(self):
        return f"Private Ad ---------------\n{self.text}\nActual until: {self.expiration_date.strftime('%d/%m/%Y')}, {self.days_left()} days left\n"


class WeatherForecast:
    def __init__(self, city, temperature, forecast):
        self.city = city
        self.temperature = temperature
        self.forecast = forecast
        self.text = f"{city}: {temperature}°C. {forecast}"

    def publish(self):
        return f"Weather Forecast ---------------\nCity: {self.city}\nTemperature: {self.temperature}°C\nForecast: {self.forecast}\n"

def preprocess_text(text):
    translator = str.maketrans('', '', string.punctuation)
    text = text.lower().translate(translator)
    return text


def analyze_words(text):
    words = text.split()
    word_count = Counter(words)

    with open('word-count.csv', 'w', newline='') as csvfile:
        fieldnames = ['word', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for word, count in word_count.items():
            writer.writerow({'word': word, 'count': count})


def analyze_letters(text):
    text = text.replace(" ", "")
    text_lower = text.lower()
    letter_count = Counter(text_lower)
    total_letters = len(text_lower)

    with open('letters.csv', 'w', newline='') as csvfile:
        fieldnames = ['letter', 'count_all', 'count_uppercase', 'percentage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for letter in string.ascii_lowercase:
            count_all = letter_count[letter]
            count_uppercase = text.count(letter.upper())
            percentage = (count_all / total_letters * 100) if total_letters > 0 else 0
            writer.writerow({'letter': letter, 'count_all': count_all, 'count_uppercase': count_uppercase,
                             'percentage': percentage})


def get_user_input():
    print("What do you want to enter?")
    print("1: News")
    print("2: Private Ad")
    print("3: Weather Forecast")

    choice = input("Enter the number of your choice: ")

    if choice == "1":
        text = input("Enter the news text: ")
        city = input("Enter the city: ")
        return News(text, city)
    elif choice == "2":
        text = input("Enter the ad text: ")
        expiration_date_str = input("Enter the expiration date (YYYY-MM-DD): ")
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
        return PrivateAd(text, expiration_date)
    elif choice == "3":
        city = input("Enter the city for the weather forecast: ")
        temperature = int(input("Enter the temperature (°C): "))
        forecast = input("Enter the weather forecast: ")
        return WeatherForecast(city, temperature, forecast)
    else:
        print("Invalid choice, please try again.")
        return None


if __name__ == "__main__":
    while True:
        record = get_user_input()
        if record:
            published_text = record.publish()
            with open('news_feed.txt', 'a', encoding='utf-8') as file:
                file.write(published_text + "\n")

            text_for_analysis = preprocess_text(record.text)
            analyze_words(text_for_analysis)
            analyze_letters(text_for_analysis)
            print("Record added and analysis updated.")

        continue_choice = input("Do you want to add another record? (yes/no): ").lower()
        if continue_choice != "yes":
            break