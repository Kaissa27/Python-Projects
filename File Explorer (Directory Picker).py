import customtkinter as ctk
from tkinter import filedialog
import threading
import yt_dlp

class YTDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pro Video Downloader v2.0")
        self.geometry("500x400")
        self.save_path = "" # Store the folder path here

        # --- UI Setup ---
        self.label = ctk.CTkLabel(self, text="YouTube URL:", font=("Arial", 14))
        self.label.pack(pady=(20, 0))

        self.url_entry = ctk.CTkEntry(self, width=400)
        self.url_entry.pack(pady=10)

        # Directory Selection
        self.path_btn = ctk.CTkButton(self, text="Select Save Folder", 
                                       fg_color="transparent", border_width=1,
                                       command=self.select_path)
        self.path_btn.pack(pady=5)
        
        self.path_label = ctk.CTkLabel(self, text="No folder selected", font=("Arial", 10), text_color="gray")
        self.path_label.pack()

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        self.btn = ctk.CTkButton(self, text="Download", command=self.start_thread, height=40)
        self.btn.pack(pady=10)

    def select_path(self):
        # Open the folder picker
        path = filedialog.askdirectory()
        if path:
            self.save_path = path
            self.path_label.configure(text=f"Saving to: {path}", text_color="white")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p_str = d.get('_percent_str', '0%').replace('%', '')
            try:
                self.progress_bar.set(float(p_str) / 100)
            except: pass

    def start_thread(self):
        url = self.url_entry.get()
        if not url or not self.save_path:
            self.path_label.configure(text="Please provide URL and Folder!", text_color="red")
            return
            
        self.btn.configure(state="disabled")
        threading.Thread(target=self.download, args=(url,), daemon=True).start()

    def download(self, url):
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{self.save_path}/%(title)s.%(ext)s', # Use the chosen path
            'progress_hooks': [self.progress_hook],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.btn.configure(state="normal")

app = YTDownloader()
app.mainloop()
