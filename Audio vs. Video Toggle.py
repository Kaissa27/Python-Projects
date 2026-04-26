import customtkinter as ctk
from tkinter import filedialog
import threading
import yt_dlp

class YouTubeMaster(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Python Pro Downloader")
        self.geometry("500x450")
        self.save_path = ""

        # --- UI ELEMENTS ---
        ctk.CTkLabel(self, text="YouTube URL:", font=("Arial", 14)).pack(pady=(20, 5))
        self.url_entry = ctk.CTkEntry(self, width=420)
        self.url_entry.pack(pady=5)

        # Format Selection (The new part!)
        ctk.CTkLabel(self, text="Select Format:", font=("Arial", 12)).pack(pady=(10, 0))
        self.format_var = ctk.StringVar(value="Video (MP4)")
        self.format_menu = ctk.CTkSegmentedButton(self, values=["Video (MP4)", "Audio (MP3)"], variable=self.format_var)
        self.format_menu.pack(pady=10)

        self.path_btn = ctk.CTkButton(self, text="📁 Choose Folder", fg_color="gray25", command=self.select_path)
        self.path_btn.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.pack()

        self.download_btn = ctk.CTkButton(self, text="DOWNLOAD", command=self.start_thread, height=50, font=("Arial", 16, "bold"))
        self.download_btn.pack(pady=20)

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.save_path = path
            self.status_label.configure(text=f"Save to: {path[:40]}...", text_color="white")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p_str = d.get('_percent_str', '0%').replace('%', '')
            try:
                self.progress_bar.set(float(p_str) / 100)
            except: pass

    def start_thread(self):
        if not self.url_entry.get() or not self.save_path:
            self.status_label.configure(text="Missing URL or Folder!", text_color="red")
            return
        
        self.download_btn.configure(state="disabled")
        threading.Thread(target=self.download_logic, daemon=True).start()

    def download_logic(self):
        url = self.url_entry.get()
        choice = self.format_var.get()
        
        # Configure options based on choice
        if choice == "Audio (MP3)":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {'format': 'bestvideo+bestaudio/best'}

        ydl_opts.update({
            'outtmpl': f'{self.save_path}/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
        })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.configure(text="Finished successfully!", text_color="green")
        except Exception as e:
            self.status_label.configure(text="Error: check URL/FFmpeg", text_color="red")
        finally:
            self.download_btn.configure(state="normal")

if __name__ == "__main__":
    app = YouTubeMaster()
    app.mainloop()
