import requests 

def get_weather(city):
    api_key = "your_api_key_here"  # Sign up at OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        print(f"In {city.title()}, it's currently {temp}°C with {desc}.")
    else:
        print("City not found or API error.")

get_weather("London")
