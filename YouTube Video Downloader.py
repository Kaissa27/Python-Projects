import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',  # Saves as the video title
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
