import sqlite3

def init_database():
    # 1. Connect to a database file (creates it if it doesn't exist)
    conn = sqlite3.connect('my_library.db')
    cursor = conn.cursor()

    # 2. Create a Table using SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    return conn

def add_book(conn, title, author):
    cursor = conn.cursor()
    # 3. Insert data safely using placeholders (?) to prevent SQL Injection
    cursor.execute('INSERT INTO books (title, author, status) VALUES (?, ?, ?)', 
                   (title, author, 'Available'))
    conn.commit()
    print(f"Added: {title}")

def find_books_by_author(conn, author):
    cursor = conn.cursor()
    # 4. Query the data
    cursor.execute('SELECT * FROM books WHERE author = ?', (author,))
    results = cursor.fetchall()
    
    print(f"\nBooks by {author}:")
    for row in results:
        print(f"ID: {row[0]} | Title: {row[1]} | Status: {row[3]}")

# Execution
connection = init_database()
add_book(connection, "The Great Gatsby", "F. Scott Fitzgerald")
add_book(connection, "1984", "George Orwell")
find_books_by_author(connection, "George Orwell")
