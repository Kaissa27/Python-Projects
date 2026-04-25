import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',  # Saves as the video title
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

import customtkinter as ctk
import threading
import yt_dlp

class YTDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pro Video Downloader")
        self.geometry("500x250")

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Paste YouTube Link Below:", font=("Arial", 16))
        self.label.pack(pady=20)

        self.url_entry = ctk.CTkEntry(self, width=400, placeholder_text="https://youtube.com/...")
        self.url_entry.pack(pady=10)

        self.btn = ctk.CTkButton(self, text="Download Video", command=self.start_download_thread)
        self.btn.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack()

    def start_download_thread(self):
        # We start the download in a separate thread so the UI stays alive
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="Please enter a URL!", text_color="red")
            return
            
        self.btn.configure(state="disabled") # Prevent multiple clicks
        self.status_label.configure(text="Downloading...", text_color="yellow")
        
        thread = threading.Thread(target=self.run_download, args=(url,))
        thread.start()

    def run_download(self, url):
        try:
            ydl_opts = {'format': 'best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.configure(text="Download Complete!", text_color="green")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)[:30]}...", text_color="red")
        finally:
            self.btn.configure(state="normal")

if __name__ == "__main__":
    app = YTDownloader()
    app.mainloop()
