import json
import os
import tkinter as tk
from tkinter import messagebox, ttk


class ExpenseTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Intermediate Expense Tracker")
        self.root.geometry("550x500")
        self.root.configure(bg="#f0f2f5")

        self.DATA_FILE = "expenses.json"
        self.expenses = self.load_data()

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # --- Form Styling & Grid ---
        form_frame = tk.LabelFrame(
            self.root,
            text=" Add New Expense ",
            font=("Arial", 11, "bold"),
            bg="#f0f2f5",
            padx=10,
            pady=10,
        )
        form_frame.pack(fill="x", padx=15, pady=10)

        # Title Input
        tk.Label(form_frame, text="Item/Title:", bg="#f0f2f5").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.title_entry = tk.Entry(form_frame, width=25)
        self.title_entry.grid(row=0, column=1, pady=5, padx=5)

        # Amount Input
        tk.Label(form_frame, text="Amount ($):", bg="#f0f2f5").grid(
            row=0, column=2, sticky="w", pady=5
        )
        self.amount_entry = tk.Entry(form_frame, width=15)
        self.amount_entry.grid(row=0, column=3, pady=5, padx=5)

        # Category Dropdown
        tk.Label(form_frame, text="Category:", bg="#f0f2f5").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.category_combobox = ttk.Combobox(
            form_frame,
            values=["Food", "Utilities", "Entertainment", "Rent", "Other"],
            width=22,
            state="readonly",
        )
        self.category_combobox.grid(row=1, column=1, pady=5, padx=5)
        self.category_combobox.current(0)

        # Submit Button
        self.add_btn = tk.Button(
            form_frame,
            text="Log Expense",
            bg="#007bff",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.add_expense,
        )
        self.add_btn.grid(row=1, column=2, columnspan=2, sticky="ew", padx=5)

        # --- Data View (Treeview) ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        columns = ("id", "title", "amount", "category")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Item")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("title", width=200, anchor="w")
        self.tree.column("amount", width=100, anchor="e")
        self.tree.column("category", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, side="left")

        # Scrollbar for table
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")

        # --- Control & Summary Footer ---
        footer_frame = tk.Frame(self.root, bg="#f0f2f5")
        footer_frame.pack(fill="x", padx=15, pady=15)

        self.total_label = tk.Label(
            footer_frame,
            text="Total Spending: $0.00",
            font=("Arial", 12, "bold"),
            bg="#f0f2f5",
        )
        self.total_label.pack(side="left")

        self.delete_btn = tk.Button(
            footer_frame,
            text="Delete Selected",
            bg="#dc3545",
            fg="white",
            command=self.delete_expense,
        )
        self.delete_btn.pack(side="right")

    # --- FUNCTIONALITY ---
    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_data(self):
        with open(self.DATA_FILE, "w") as f:
            json.dump(self.expenses, f, indent=4)

    def refresh_table(self):
        # Clear existing views
        for item in self.tree.get_children():
            self.tree.delete(item)

        total = 0.0
        for index, exp in enumerate(self.expenses):
            self.tree.insert(
                "",
                "end",
                values=(index, exp["title"], f"${exp['amount']:.2f}", exp["category"]),
            )
            total += exp["amount"]

        self.total_label.config(text=f"Total Spending: ${total:.2f}")

    def add_expense(self):
        title = self.title_entry.get().strip()
        amount_raw = self.amount_entry.get().strip()
        category = self.category_combobox.get()

        if not title or not amount_raw:
            messagebox.showwarning("Error", "Please fill in all input fields.")
            return

        try:
            amount = float(amount_raw)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid positive number for amount."
            )
            return

        new_expense = {"title": title, "amount": amount, "category": category}

        self.expenses.append(new_expense)
        self.save_data()
        self.refresh_table()

        # Clear Inputs
        self.title_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "No item selected to delete.")
            return

        item_data = self.tree.item(selected_item)["values"]
        item_id = int(item_data[0])  # The index in our structural list

        del self.expenses[item_id]
        self.save_data()
        self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
