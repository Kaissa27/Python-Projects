import sys

def get_condition_style(condition):
    styles = {
        "Sunny": "Clear Skies",
        "Rainy": "Heavy Rain",
        "Cloudy": "Overcast",
        "Snowy": "Blizzard Warning"
    }
    return styles.get(condition, "Stable")

def display_weather(city, data):
    print(f"\nWeather Report: {city.upper()}")
    print("-" * 30)
    
    temp_c = data["temp"]
    temp_f = (temp_c * 9/5) + 32
    condition = data["condition"]
    style = get_condition_style(condition)
    
    print(f"Condition: {condition} ({style})")
    print(f"Temperature: {temp_c}°C / {temp_f:.1f}°F")
    print(f"Humidity: {data['humidity']}%")
    print(f"Wind Speed: {data['wind']} km/h")
    
    if temp_c > 30:
        print("Status: Heat Advisory")
    elif temp_c < 0:
        print("Status: Freezing Warning")
    else:
        print("Status: Normal Conditions")

def main():
    weather_db = {
        "London": {"temp": 15, "condition": "Cloudy", "humidity": 80, "wind": 12},
        "Dubai": {"temp": 42, "condition": "Sunny", "humidity": 15, "wind": 8},
        "New York": {"temp": -2, "condition": "Snowy", "humidity": 60, "wind": 25},
        "Mumbai": {"temp": 31, "condition": "Rainy", "humidity": 90, "wind": 15}
    }

    while True:
        print("\nGlobal Weather Tracker")
        city = input("Enter City Name (or 'exit'): ").strip().title()
        
        if city.lower() == 'exit':
            sys.exit()
            
        if city in weather_db:
            display_weather(city, weather_db[city])
        else:
            print("City data not available in offline database.")

if __name__ == "__main__":
    main()