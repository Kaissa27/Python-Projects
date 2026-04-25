import customtkinter as ctk
import threading
import yt_dlp
import re

class YTDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pro Downloader with Progress")
        self.geometry("500x350")

        self.label = ctk.CTkLabel(self, text="YouTube URL:", font=("Arial", 14))
        self.label.pack(pady=(20, 0))

        self.url_entry = ctk.CTkEntry(self, width=400)
        self.url_entry.pack(pady=10)

        # Progress Bar (initially set to 0)
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Ready", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.btn = ctk.CTkButton(self, text="Start Download", command=self.start_thread)
        self.btn.pack(pady=20)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # Clean the percentage string (e.g., ' 45.2%' -> 0.452)
            p_str = d.get('_percent_str', '0%').replace('%', '')
            try:
                p_float = float(p_str) / 100
                self.progress_bar.set(p_float)
                self.status_label.configure(text=f"Downloading: {p_str}%")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_bar.set(1.0)
            self.status_label.configure(text="Download Complete! Finalizing...")

    def start_thread(self):
        url = self.url_entry.get()
        if url:
            self.btn.configure(state="disabled")
            threading.Thread(target=self.download, args=(url,), daemon=True).start()

    def download(self, url):
        ydl_opts = {
            'format': 'best',
            'progress_hooks': [self.progress_hook],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.configure(text="Success!", text_color="green")
        except Exception as e:
            self.status_label.configure(text="Error occurred", text_color="red")
        finally:
            self.btn.configure(state="normal")

app = YTDownloader()
app.mainloop()
