import sqlite3  

class LibraryDB:
    def __init__(self, db_name="library.db"):
        # Connect to the database (it creates the file if it doesn't exist)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create a table using SQL syntax
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                available BOOLEAN DEFAULT 1
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author, year):
        # Using ? as placeholders to prevent SQL Injection (security best practice)
        self.cursor.execute('''
            INSERT INTO books (title, author, year) VALUES (?, ?, ?)
        ''', (title, author, year))
        self.conn.commit()
        print(f"Added: {title}")

    def find_books_by_author(self, author):
        self.cursor.execute("SELECT * FROM books WHERE author = ?", (author,))
        results = self.cursor.fetchall()
        
        print(f"\nBooks by {author}:")
        for row in results:
            status = "Available" if row[4] else "Checked Out"
            print(f"ID: {row[0]} | {row[1]} ({row[3]}) - {status}")

    def close(self):
        self.conn.close()

# Implementation
db = LibraryDB()
db.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
db.add_book("Tender is the Night", "F. Scott Fitzgerald", 1934)
db.find_books_by_author("F. Scott Fitzgerald")
db.close()
