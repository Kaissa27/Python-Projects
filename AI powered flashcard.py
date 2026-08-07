import sqlite3
import datetime
import random
from rich.console import Console
from rich.prompt import Prompt

console = Console()
DB = "flashcards.db"

class Card:
    def __init__(self, id, front, back, interval=0, repetition=0, ef=2.5, due_date=None):
        self.id = id
        self.front = front
        self.back = back
        self.interval = interval # days
        self.repetition = repetition
        self.ef = ef # easiness factor
        self.due_date = due_date or datetime.date.today()

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS cards
                 (id INTEGER PRIMARY KEY, front TEXT, back TEXT,
                  interval REAL, repetition INTEGER, ef REAL, due_date TEXT)''')
    conn.commit()
    conn.close()

def update_card(card, quality): # quality 0-5, 5=perfect
    if quality < 3:
        card.repetition = 0
        card.interval = 1
    else:
        if card.repetition == 0: card.interval = 1
        elif card.repetition == 1: card.interval = 6
        else: card.interval = round(card.interval * card.ef)
        card.repetition += 1

    card.ef = card.ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if card.ef < 1.3: card.ef = 1.3

    card.due_date = datetime.date.today() + datetime.timedelta(days=card.interval)

def quiz():
    conn = sqlite3.connect(DB)
    today = datetime.date.today().isoformat()
    cards = conn.execute("SELECT * FROM cards WHERE due_date <=?", (today,)).fetchall()

    if not cards:
        console.print("[green]No cards due today! [/green]")
        return

    random.shuffle(cards)
    for c in cards:
        card = Card(*c)
        console.print(f"\n[bold]Q:[/bold] {card.front}")
        input("Press Enter to see answer...")
        console.print(f"[bold]A:[/bold] {card.back}")

        quality = int(Prompt.ask("How well did you recall? 0=Forgot 5=Easy", choices=["0","1","2","3","4","5"]))
        update_card(card, quality)

        conn.execute("UPDATE cards SET interval=?, repetition=?, ef=?, due_date=? WHERE id=?",
                     (card.interval, card.repetition, card.ef, card.due_date.isoformat(), card.id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    while True:
        choice = Prompt.ask("\n1. Add Card 2. Quiz 3. Exit", choices=["1","2","3"])
        if choice == "1":
            f = input("Front: ")
            b = input("Back: ")
            conn = sqlite3.connect(DB)
            conn.execute("INSERT INTO cards(front,back) VALUES (?,?)", (f,b))
            conn.commit(); conn.close()
        elif choice == "2": quiz()
        else: break