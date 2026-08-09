import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

FILE = "expenses.csv"

# Create file with headers if it doesn't exist
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Description", "Amount"])

def add_expense():
    date = datetime.now().strftime("%Y-%m-%d")
    category = input("Category (Food, Transport, Manga, Bills, Other): ")
    desc = input("Description: ")
    amount = float(input("Amount ₹: "))
    
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, desc, amount])
    print("Expense added!")

def view_expenses():
    df = pd.read_csv(FILE)
    if df.empty:
        print("No expenses yet.")
        return
    print("\n--- All Expenses ---")
    print(df.to_string(index=False))
    print(f"\nTotal Spent: ₹{df['Amount'].sum():.2f}")

def show_summary():
    df = pd.read_csv(FILE)
    if df.empty:
        print("No data to summarize.")
        return
    
    summary = df.groupby("Category")["Amount"].sum()
    print("\n--- Spending by Category ---")
    print(summary)
    
    # Plot pie chart
    summary.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Monthly Spending Breakdown")
    plt.ylabel("")
    plt.show()

def main():
    while True:
        print("\n1. Add Expense")
        print("2. View All Expenses")
        print("3. Show Summary + Chart")
        print("4. Exit")
        choice = input("Choose: ")
        
        if choice == "1": add_expense()
        elif choice == "2": view_expenses()
        elif choice == "3": show_summary()
        elif choice == "4": break
        else: print("Invalid choice")

if __name__ == "__main__":
    main()