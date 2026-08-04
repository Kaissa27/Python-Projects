import streamlit as st
import requests

API_KEY = "YOUR_OPENWEATHER_KEY"
CITY = "Kolkata"

st.title("🌤️ Kolkata Outfit Recommender")

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()
    return {
        "temp":