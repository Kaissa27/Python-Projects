import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
import time
from email.mime.text import MIMEText

# ===== SETTINGS =====
PRODUCT_URL = "PASTE_AMAZON_PRODUCT_LINK_HERE" 
TARGET_PRICE = 20000  # Alert me if below Rs 20000
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password" # Use Gmail App Password, not normal password
RECEIVER_EMAIL = "your_email@gmail.com"
# ====================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_price():
    response = requests.get(PRODUCT_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Amazon price is usually in span.a-offscreen
    price_tag = soup.find("span", class_="a-offscreen")
    product_title = soup.find("span", id="productTitle").get_text().strip()
    
    if price_tag:
        price_text = price_tag.get_text()
        price = float(price_text.replace("₹", "").replace(",", ""))
        return product_title, price
    return None, None

def send_email(title, price):
    msg = MIMEText(f"Price Drop Alert!\n\n{title}\nCurrent Price: ₹{price}\nLink: {PRODUCT_URL}")
    msg["Subject"] = f"Price Drop: ₹{price}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    print("Email sent!")

def check_price():
    print("Checking price...")
    title, price = get_price()
    if price and price < TARGET_PRICE:
        print(f"Price dropped to ₹{price}!")
        send_email(title, price)
    else:
        print(f"Current price: ₹{price}. Still above target.")

# Run every 6 hours
schedule.every(6).hours.do(check_price)
check_price() # run once immediately

print("Tracker started. Will check every 6 hours...")
while True:
    schedule.run_pending()
    time.sleep(60)