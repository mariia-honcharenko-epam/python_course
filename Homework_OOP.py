from datetime import datetime, timedelta


class News:

    def __init__(self, text, city):
        self.text = text

        self.city = city

        self.publish_date = datetime.now()

    def publish(self):
        return f"News ---------------\n{self.text}\n{self.city}, {self.publish_date.strftime('%d/%m/%Y %H.%M')}\n"


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

    def publish(self):
        return f"Weather Forecast ---------------\nCity: {self.city}\nTemperature: {self.temperature}°C\nForecast: {self.forecast}\n"


# Функція для взаємодії з користувачем

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

        expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d")

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

        if record is not None:
            with open("news_feed.txt", "a") as file:
                file.write(record.publish())

            print("Record added to the file successfully.")

        continue_choice = input("Do you want to add another record? (yes/no): ").lower()

        if continue_choice != "yes":
            break
