import tkinter as tk 
from tkinter import messagebox

def save_file():
    # Get all text from the start (1.0) to the end (end)
    content = text_area.get("1.0", tk.END)
    
    with open("my_note.txt", "w") as f:
        f.write(content)
    
    # Show a pop-up confirmation
    messagebox.showinfo("Success", "Note saved to my_note.txt!")

# 1. Create the Main Window
root = tk.Tk()
root.title("Python Notepad")
root.geometry("400x400")

# 2. Add a Label (Title)
label = tk.Label(root, text="Type your notes below:", font=("Arial", 12))
label.pack(pady=10)

# 3. Add a Text Entry Area
text_area = tk.Text(root, height=15, width=45)
text_area.pack(padx=20)

# 4. Add a Save Button
# The 'command' tells the button which function to run when clicked
save_btn = tk.Button(root, text="Save Note", command=save_file, bg="green", fg="white")
save_btn.pack(pady=10)

# 5. Start the App
root.mainloop()
