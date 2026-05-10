import tkinter as tk
import requests
from tkinter import messagebox

def get_weather():
    city = city_entry.get()
    # In a real app, you'd use: f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    # For now, let's look at how we handle the 'JSON' data that comes back:
    
    try:
        # Simulated API Response (JSON is just a big Python Dictionary)
        weather_data = {
            "main": {"temp": 22.5, "humidity": 60},
            "weather": [{"description": "clear sky"}]
        }
        
        temp = weather_data['main']['temp']
        desc = weather_data['weather'][0]['description']
        
        result_label.config(text=f"Temp: {temp}°C\nSky: {desc.capitalize()}")
        
    except Exception:
        messagebox.showerror("Error", "City not found!")

# --- GUI Setup ---
root = tk.Tk()
root.title("SkyCast")
root.geometry("300x250")
root.configure(bg="#1a1a1a")

# Input
city_entry = tk.Entry(root, font=("Arial", 14), bg="#333", fg="white", insertbackground="white")
city_entry.pack(pady=20, padx=20)

# Button
search_btn = tk.Button(root, text="Check Weather", command=get_weather, 
                       bg="#00d1b2", fg="white", font=("Arial", 10, "bold"))
search_btn.pack(pady=10)

# Display
result_label = tk.Label(root, text="Enter a city above", font=("Arial", 12), 
                        bg="#1a1a1a", fg="#aaa")
result_label.pack(pady=20)

root.mainloop()
