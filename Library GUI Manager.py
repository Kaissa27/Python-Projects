import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# --- DATABASE LOGIC (The Model) ---
def init_db():
    conn = sqlite3.connect("library_gui.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                      (id INTEGER PRIMARY KEY, title TEXT, author TEXT)''')
    conn.commit()
    conn.close()

def add_to_db(title, author):
    conn = sqlite3.connect("library_gui.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

# --- GUI LOGIC (The View) ---
class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SQL Book Manager")
        self.geometry("400x450")
        
        init_db()

        # Input Fields
        self.label = ctk.CTkLabel(self, text="Library System", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Book Title", width=300)
        self.title_entry.pack(pady=10)

        self.author_entry = ctk.CTkEntry(self, placeholder_text="Author", width=300)
        self.author_entry.pack(pady=10)

        # Buttons
        self.add_btn = ctk.CTkButton(self, text="Add to Database", command=self.save_book)
        self.add_btn.pack(pady=20)

        self.view_btn = ctk.CTkButton(self, text="Show All Books", fg_color="transparent", 
                                      border_width=1, command=self.show_books)
        self.view_btn.pack(pady=10)

    def save_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        
        if title and author:
            add_to_db(title, author)
            self.title_entry.delete(0, 'end')
            self.author_entry.delete(0, 'end')
            messagebox.showinfo("Success", f"'{title}' added to database!")
        else:
            messagebox.showwarning("Error", "Please fill in all fields")

    def show_books(self):
        conn = sqlite3.connect("library_gui.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        conn.close()
        
        # Displaying in a simple popup for now
        book_list = "\n".join([f"{r[1]} by {r[2]}" for r in rows])
        messagebox.showinfo("Inventory", book_list if book_list else "Library is empty!")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
