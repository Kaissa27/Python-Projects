import customtkinter as ctk

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern Task Manager")
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Tasks for Today", font=("Arial", 20))
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter a task...")
        self.entry.pack(pady=10)

        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

    def add_task(self):
        task = self.entry.get()
        if task:
            print(f"Task Added: {task}") # Replace with UI list logic
            self.entry.delete(0, 'end')

app = TodoApp()
app.mainloop()
