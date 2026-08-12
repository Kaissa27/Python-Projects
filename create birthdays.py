import pandas as pd
import schedule
import time
from datetime import datetime, timedelta
import random

# Gift ideas by relation
GIFT_IDEAS = {
    "Friend": ["Hoodie", "Bluetooth speaker", "Board game", "Cake + movie night"],
    "Family": ["Watch", "Perfume", "Wallet", "Dinner treat"],
    "Cousin": ["Gaming voucher", "Headphones", "Book", "Sneakers"],
    "default": ["Chocolate hamper", "Gift card", "Plant", "Personalized mug"]
}

def get_gift_ideas(relation):
    ideas = GIFT_IDEAS.get(relation, GIFT_IDEAS["default"])
    return random.sample(ideas, 3)

def check_birthdays():
    df = pd.read_csv("birthdays.csv")
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    for _, row in df.iterrows():
        bday = datetime.strptime(row["Date"], "%d-%m-%Y").date()
        # Compare only day and month
        if bday.replace(year=tomorrow.year) == tomorrow:
            name = row["Name"]
            relation = row["Relation"]
            gifts = get_gift_ideas(relation)
            
            print("\n🎉 BIRTHDAY REMINDER 🎉")
            print(f"{name} ({relation}) has birthday tomorrow - {tomorrow.strftime('%d %B')}")
            print(f"Gift Ideas: {', '.join(gifts)}")
            print(f"WhatsApp them: https://wa.me/91{row['Phone']}")
            print("-" * 40)
            
            # Here you can add pywhatkit or selenium to auto-send WhatsApp message
            # but manual is safer for now

print("Bot started! Checking birthdays every day at 9 AM...")
schedule.every().day.at("09:00").do(check_birthdays)
check_birthdays() # run once now

while True:
    schedule.run_pending()
    time.sleep(60)