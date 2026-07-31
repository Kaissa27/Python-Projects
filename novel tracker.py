import sqlite3
import requests
from bs4 import BeautifulSoup
import schedule
import time
from plyer import notification

DB = "manga_tracker.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS manga
                 (id INTEGER PRIMARY KEY, title TEXT, url TEXT, current_ch REAL)''')
    conn.commit()
    conn.close()

def add_manga():
    title = input("Manga/Novel name: ")
    url = input("Link to manga page: ")
    ch = float(input("Current chapter: "))
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO manga (title, url, current_ch) VALUES (?,?,?)", (title, url, ch))
    conn.commit()
    conn.close()
    print(f"✅ Added {title}")

def check_updates():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    for id, title, url, current_ch in c.execute("SELECT * FROM manga"):
        # Example: scrape latest chapter
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        latest_ch = float(soup.select_one('.chapter-name').text.split()[1]) # adjust selector

        if latest_ch > current_ch:
            notification.notify(
                title=f"New Chapter: {title}",
                message=f"Chapter {latest_ch} is out!",
                timeout=10
            )
            c.execute("UPDATE manga SET current_ch=? WHERE id=?", (latest_ch, id))
    conn.commit()
    conn.close()

def main():
    init_db()
    schedule.every(6).hours.do(check_updates)
    print("Tracker running... checking every 6 hours")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()