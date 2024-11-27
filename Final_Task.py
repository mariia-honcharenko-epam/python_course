from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="geoapi_exercise")
    location = geolocator.geocode(city_name)
    if location:
        return (location.latitude, location.longitude)
    else:
        print(f"Coordinates for {city_name} couldn't be found.")
        try:
            lat = float(input(f"Please enter the latitude for {city_name}: "))
            lon = float(input(f"Please enter the longitude for {city_name}: "))
            return (lat, lon)
        except ValueError:
            print("Invalid input. Please enter valid latitude and longitude.")
            return None

def calculate_distance(coords1, coords2):
    if not coords1 or not coords2:
        print("Cannot calculate distance with invalid coordinates.")
        return None
    distance = geodesic(coords1, coords2).kilometers
    return distance

def main():
    city1 = input("Enter the name of the first city: ")
    city2 = input("Enter the name of the second city: ")

    coords1 = get_coordinates(city1)
    coords2 = get_coordinates(city2)

    if coords1 and coords2:
        distance = calculate_distance(coords1, coords2)
        print(f"The distance between {city1} and {city2} is approximately {distance:.2f} kilometers.")

if __name__ == "__main__":
    main()