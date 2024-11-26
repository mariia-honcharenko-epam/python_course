import os
import csv
import json
import string
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
import psycopg2

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


class DBConnection:
    def __init__(self, database_name="news_database", user="postgres", password="Bohatyrska!32", host="localhost", port=5432):
        try:
            self.conn = psycopg2.connect(
                dbname=database_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cur = self.conn.cursor()
            self.create_tables()
            print("Connected to PostgreSQL successfully!")
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def create_tables(self):
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id SERIAL PRIMARY KEY,
                    text TEXT,
                    city TEXT,
                    publish_date TIMESTAMP
                );
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS private_ads (
                    id SERIAL PRIMARY KEY,
                    text TEXT,
                    expiration_date DATE
                );
            """)
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS weather_forecasts (
                    id SERIAL PRIMARY KEY,
                    city TEXT,
                    temperature INTEGER,
                    forecast TEXT
                );
            """)
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error creating tables: {e}")

    def insert(self, table_name, data):
        try:
            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join(data.keys())
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cur.execute(sql, list(data.values()))
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error inserting data into {table_name}: {e}")

    def check_duplicate(self, table_name, column, value):
        self.cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column} = %s", (value,))
        result = self.cur.fetchone()
        return result[0] > 0 if result else False

    def close(self):
        self.cur.close()
        self.conn.close()
        print("Connection closed.")

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
        writer = csv.DictWriter(csvfile, fieldnames=['word', 'count'])
        for word, count in word_count.items():
            writer.writerow({'word': word, 'count': count})

def analyze_letters(text):
    text = text.replace(" ", "")
    letter_count = Counter(text.lower())
    total_letters = len(text)
    write_header_if_needed('letters.csv', ['letter', 'count'])
    with open('letters.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['letter', 'count'])
        for letter, count in letter_count.items():
            writer.writerow({'letter': letter, 'count': count})

def get_user_input(db_conn):
    print("How would you like to input data?")
    print("1: Manual Entry")
    print("2: JSON File Entry")
    print("3: XML File Entry")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        return manual_entry(db_conn)
    elif choice == "2":
        return setup_json_file_entry(db_conn)
    elif choice == "3":
        return setup_xml_file_entry(db_conn)
    else:
        print("Invalid choice, please try again.")
        return None

def manual_entry(db_conn):
    print("What do you want to enter?")
    print("1: News")
    print("2: Private Ad")
    print("3: Weather Forecast")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        text = input("Enter the news text: ")
        city = input("Enter the city: ")
        news = News(text, city)
        if not db_conn.check_duplicate("news", "text", news.text) and not db_conn.check_duplicate("news", "city", news.city):
            db_conn.insert('news', {'text': news.text, 'city': news.city, 'publish_date': datetime.now()})
        return [news]
    elif choice == "2":
        text = input("Enter the ad text: ")
        expiration_date_str = input("Enter the expiration date (YYYY-MM-DD): ")
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
        ad = PrivateAd(text, expiration_date)
        if not db_conn.check_duplicate("private_ads", "text", ad.text):
            db_conn.insert('private_ads', {'text': ad.text, 'expiration_date': ad.expiration_date})
        return [ad]
    elif choice == "3":
        city = input("Enter the city for the weather forecast: ")
        temperature = int(input("Enter the temperature (°C): "))
        forecast = input("Enter the weather forecast: ")
        weather = WeatherForecast(city, temperature, forecast)
        if not db_conn.check_duplicate("weather_forecasts", "city", weather.city):
            db_conn.insert('weather_forecasts', {'city': weather.city, 'temperature': weather.temperature, 'forecast': weather.forecast})
        return [weather]
    else:
        print("Invalid choice, please try again.")
        return []

def setup_json_file_entry(db_conn):
    dir_name = "json_uploads"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    print(f"Please place your JSON file in the '{dir_name}' directory and name it 'data.json'. Then press any key to continue.")
    input("Press any key to continue after placing JSON file...")
    return load_json_from_file(dir_name, db_conn)

def setup_xml_file_entry(db_conn):
    dir_name = "xml_uploads"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    print(f"Please place your XML file in the '{dir_name}' directory and name it 'data.xml'. Then press any key to continue.")
    input("Press any key to continue after placing XML file...")
    return load_xml_from_file(dir_name, db_conn)

def load_json_from_file(directory, db_conn):
    file_path = os.path.join(directory, "data.json")
    if not os.path.exists(file_path):
        print("File not found. Please ensure the file is placed correctly and named 'data.json'.")
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            items = json.load(file)
            return process_json_data(items, db_conn)
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return []

def load_xml_from_file(directory, db_conn):
    file_path = os.path.join(directory, "data.xml")
    if not os.path.exists(file_path):
        print("File not found. Please ensure the file is placed correctly and named 'data.xml'.")
        return []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return process_xml_data(root, db_conn)
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return []

def process_json_data(items, db_conn):
    records = []
    for item in items:
        type_ = item['type']
        data = item['data']
        if type_ == "news":
            news = News(data['text'], data['city'])
            if not db_conn.check_duplicate("news", "text", news.text) and not db_conn.check_duplicate("news", "city", news.city):
                db_conn.insert('news', {'text': news.text, 'city': news.city, 'publish_date': datetime.now()})
            records.append(news)
        elif type_ == "private_ad":
            expiration_date = datetime.strptime(data['expiration_date'], '%Y-%m-%d')
            ad = PrivateAd(data['text'], expiration_date)
            if not db_conn.check_duplicate("private_ads", "text", ad.text):
                db_conn.insert('private_ads', {'text': ad.text, 'expiration_date': expiration_date})
            records.append(ad)
        elif type_ == "weather_forecast":
            weather = WeatherForecast(data['city'], int(data['temperature']), data['forecast'])
            if not db_conn.check_duplicate("weather_forecasts", "city", weather.city):
                db_conn.insert('weather_forecasts', {'city': weather.city, 'temperature': weather.temperature, 'forecast': weather.forecast})
            records.append(weather)
        else:
            print(f"Unrecognized type {type_}")
    return records

def process_xml_data(root, db_conn):
    records = []
    for child in root:
        type_ = child.tag
        data = child.attrib
        if type_ == "news":
            news = News(data['text'], data['city'])
            if not db_conn.check_duplicate("news", "text", news.text) and not db_conn.check_duplicate("news", "city", news.city):
                db_conn.insert('news', {'text': news.text, 'city': news.city, 'publish_date': datetime.now()})
            records.append(news)
        elif type_ == "private_ad":
            expiration_date = datetime.strptime(data['expiration_date'], '%Y-%m-%d')
            ad = PrivateAd(data['text'], expiration_date)
            if not db_conn.check_duplicate("private_ads", "text", ad.text):
                db_conn.insert('private_ads', {'text': ad.text, 'expiration_date': expiration_date})
            records.append(ad)
        elif type_ == "weather_forecast":
            weather = WeatherForecast(data['city'], int(data['temperature']), data['forecast'])
            if not db_conn.check_duplicate("weather_forecasts", "city", weather.city):
                db_conn.insert('weather_forecasts', {'city': weather.city, 'temperature': weather.temperature, 'forecast': weather.forecast})
            records.append(weather)
        else:
            print(f"Unrecognized type {type_}")
    return records

if __name__ == "__main__":
    db_conn = DBConnection()
    while True:
        records = get_user_input(db_conn)
        if records:
            for record in records:
                published_text = record.publish()
                print(f"Attempting to write to file: {published_text}")
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
    db_conn.close()