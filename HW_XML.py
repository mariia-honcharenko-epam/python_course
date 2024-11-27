import os
import json
from datetime import datetime
import csv
import string
import xml.etree.ElementTree as ET
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

def write_header_if_needed(filename, fieldnames):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

def analyze_words(text):
    words = text.split()
    word_count = Counter(words)
    write_header_if_needed('word-count.csv', ['word', 'count'])
    with open('word-count.csv', 'a', newline='') as csvfile:
        fieldnames = ['word', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for word, count in word_count.items():
            writer.writerow({'word': word, 'count': count})

def analyze_letters(text):
    text = text.replace(" ", "")
    text_lower = text.lower()
    letter_count = Counter(text_lower)
    total_letters = len(text_lower)
    write_header_if_needed('letters.csv', ['letter', 'count_all', 'count_uppercase', 'percentage'])
    with open('letters.csv', 'a', newline='') as csvfile:
        fieldnames = ['letter', 'count_all', 'count_uppercase', 'percentage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for letter in string.ascii_lowercase:
            count_all = letter_count[letter]
            count_uppercase = text.count(letter.upper())
            percentage = (count_all / total_letters * 100) if total_letters > 0 else 0
            writer.writerow({'letter': letter, 'count_all': count_all, 'count_uppercase': count_uppercase, 'percentage': percentage})

def get_user_input():
    print("How would you like to input data?")
    print("1: Manual Entry")
    print("2: JSON File Entry")
    print("3: XML File Entry")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        return manual_entry()
    elif choice == "2":
        return setup_json_file_entry()
    elif choice == "3":
        return setup_xml_file_entry()
    else:
        print("Invalid choice, please try again.")
        return None

def manual_entry():
    print("What do you want to enter?")
    print("1: News")
    print("2: Private Ad")
    print("3: Weather Forecast")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        text = input("Enter the news text: ")
        city = input("Enter the city: ")
        return [News(text, city)]
    elif choice == "2":
        text = input("Enter the ad text: ")
        expiration_date_str = input("Enter the expiration date (YYYY-MM-DD): ")
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
        return [PrivateAd(text, expiration_date)]
    elif choice == "3":
        city = input("Enter the city for the weather forecast: ")
        temperature = int(input("Enter the temperature (°C): "))
        forecast = input("Enter the weather forecast: ")
        return [WeatherForecast(city, temperature, forecast)]
    else:
        print("Invalid choice, please try again.")
        return []

def setup_json_file_entry():
    dir_name = "json_uploads"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    print(f"Please place your JSON file in the '{dir_name}' directory and name it 'data.json'. Then press any key to continue.")
    input("Press any key to continue after placing JSON file...")
    return load_json_from_file(dir_name)

def setup_xml_file_entry():
    dir_name = "xml_uploads"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    print(f"Please place your XML file in the '{dir_name}' directory and name it 'data.xml'. Then press any key to continue.")
    input("Press any key to continue after placing XML file...")
    return load_xml_from_file(dir_name)

def load_json_from_file(directory):
    file_path = os.path.join(directory, "data.json")
    if not os.path.exists(file_path):
        print("File not found. Please ensure the file is placed correctly and named 'data.json'.")
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            items = json.load(file)
            return process_json_data(items)
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return []

def load_xml_from_file(directory):
    file_path = os.path.join(directory, "data.xml")
    if not os.path.exists(file_path):
        print("File not found. Please ensure the file is placed correctly and named 'data.xml'.")
        return []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return process_xml_data(root)
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return []

def process_json_data(items):
    records = []
    for item in items:
        type_ = item['type']
        data = item['data']
        if type_ == "news":
            records.append(News(data['text'], data['city']))
        elif type_ == "private_ad":
            expiration_date = datetime.strptime(data['expiration_date'], '%Y-%m-%d')
            records.append(PrivateAd(data['text'], expiration_date))
        elif type_ == "weather_forecast":
            records.append(WeatherForecast(data['city'], int(data['temperature']), data['forecast']))
        else:
            print(f"Unrecognized type {type_}")
    return records

def process_xml_data(root):
    records = []
    for child in root:
        type_ = child.tag
        data = child.attrib
        if type_ == "news":
            records.append(News(data['text'], data['city']))
        elif type_ == "private_ad":
            expiration_date = datetime.strptime(data['expiration_date'], '%Y-%m-%d')
            records.append(PrivateAd(data['text'], expiration_date))
        elif type_ == "weather_forecast":
            records.append(WeatherForecast(data['city'], int(data['temperature']), data['forecast']))
        else:
            print(f"Unrecognized type {type_}")
    return records

if __name__ == "__main__":
    while True:
        records = get_user_input()
        if records:
            for record in records:
                published_text = record.publish()
                print(f"Attempting to write to file: {published_text}")  # Debug statement
                try:
                    with open('news_feed.txt', 'a', encoding='utf-8') as file:
                        file.write(published_text + "\n")
                    print("Write successful")
                except Exception as e:
                    print(f"Failed to write to file: {str(e)}")
                text_for_analysis = preprocess_text(record.text)
                analyze_words(text_for_analysis)
                analyze_letters(text_for_analysis)
            print("Record added and analysis updated.")
        continue_choice = input("Do you want to add another record? (yes/no): ").lower()
        if continue_choice != "yes":
            break