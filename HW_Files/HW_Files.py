import os
from datetime import datetime

from text_utils.normalization import normalize_text

class News:
    def __init__(self, text, datetime_info):
        self.text = normalize_text(text)
        self.datetime_info = datetime_info

    def publish(self):
        return f"News ---------------\n{self.text}\n{self.datetime_info}\n"

class PrivateAd:
    def __init__(self, text, expiration_details):
        self.text = normalize_text(text)
        self.expiration_details = expiration_details

    def publish(self):
        return f"Private Ad ---------------\n{self.text}\n{self.expiration_details}\n"

class WeatherForecast:
    def __init__(self, city, temperature, forecast):
        self.city = city.title()
        self.temperature = temperature
        self.forecast = normalize_text(forecast)

    def publish(self):
        return f"Weather Forecast ---------------\nCity: {self.city}\nTemperature: {self.temperature}°C\nForecast: {self.forecast}\n"

def ensure_directory_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' was created.")
    else:
        print(f"Folder '{folder_name}' already exists.")

def process_file(input_folder, input_filename):
    input_path = os.path.join(input_folder, input_filename)
    if not os.path.exists(input_path):
        print(f"No input file exists at {input_path}")
        return

    records = []
    current_block = []
    block_type = None

    with open(input_path, "r", encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if "News ---------------" in line:
                if current_block:
                    records.append(process_block(block_type, current_block))
                block_type = 'News'
                current_block = []
            elif "Private Ad ---------------" in line:
                if current_block:
                    records.append(process_block(block_type, current_block))
                block_type = 'Private Ad'
                current_block = []
            elif "Weather Forecast ---------------" in line:
                if current_block:
                    records.append(process_block(block_type, current_block))
                block_type = 'Weather Forecast'
                current_block = []
            else:
                current_block.append(line)

    if current_block:
        records.append(process_block(block_type, current_block))

    output_path = os.path.join(input_folder, "news_feed.txt")
    with open(output_path, "a", encoding='utf-8') as file:
        for record in records:
            file.write(record + '\n')

    print(f"Data from '{input_filename}' has been processed and added to 'news_feed.txt'")

def process_block(block_type, content):
    if block_type == 'News':
        return News(content[0], content[1]).publish()
    elif block_type == 'Private Ad':
        return PrivateAd(content[0], content[1]).publish()
    elif block_type == 'Weather Forecast':
        city = content[0].split(":")[1].strip()
        temperature = content[1].split(":")[1].strip("°C ").strip()
        forecast = content[2].split(":")[1].strip()
        return WeatherForecast(city, temperature, forecast).publish()

if __name__ == "__main__":
    folder_name = "TextFileInput"
    input_filename = "input_data.txt"

    ensure_directory_exists(folder_name)
    process_file(folder_name, input_filename)