import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

def track_price():
    # Example URL (using a dummy site for practice)
    url = 'https://www.example-store.com/product-123'
    headers = {"User-Agent": "Mozilla/5.0"}

    # 1. Fetch and Parse
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 2. Extract Price (Logic depends on the site's HTML)
    # Let's assume the price is in <span class="price-amount">
    price_text = soup.find("span", class_="price-amount").get_text()
    
    # Clean the data: "$1,200.50" -> 1200.50
    current_price = float(price_text.replace("$", "").replace(",", ""))

    # 3. Save to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile('price_log.csv')

    with open('price_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Add header if it's a new file
        if not file_exists:
            writer.writerow(['Timestamp', 'Price'])
        writer.writerow([timestamp, current_price])

    print(f"Logged ${current_price} at {timestamp}")

# track_price()
