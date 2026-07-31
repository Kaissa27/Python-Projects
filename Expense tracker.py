import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, type TEXT, category TEXT, 
                  amount REAL, date TEXT, note TEXT)''')
    conn.commit()
    conn.close()

def add_transaction():
    t_type = input("Income or Expense? ").lower()
    category = input("Category e.g. Food, Rent, Salary: ")
    amount = float(input("Amount: ₹"))
    note = input("Note: ")
    date = datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO transactions (type, category, amount, date, note) VALUES (?,?,?,?,?)",
              (t_type, category, amount, date, note))
    conn.commit()
    conn.close()
    print("✅ Transaction added!")

def view_summary():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    
    if df.empty:
        print("No transactions yet.")
        return
    
    income = df[df['type']=='income']['amount'].sum()
    expense = df[df['type']=='expense']['amount'].sum()
    balance = income - expense
    
    print(f"\n--- Summary ---")
    print(f"Total Income:  ₹{income}")
    print(f"Total Expense: ₹{expense}")
    print(f"Balance:       ₹{balance}")
    
    # Plot expense by category
    expense_df = df[df['type']=='expense']
    if not expense_df.empty:
        expense_df.groupby('category')['amount'].sum().plot(kind='bar')
        plt.title("Spending by Category")
        plt.ylabel("Amount ₹")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def main():
    init_db()
    while True:
        print("\n1. Add Transaction\n2. View Summary\n3. Exit")
        choice = input("Choose: ")
        if choice == '1': add_transaction()
        elif choice == '2': view_summary()
        elif choice == '3': break
        else: print("Invalid choice")

if __name__ == "__main__":
    main()