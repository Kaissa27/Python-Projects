import time
from datetime import datetime
import os

# Windows path. For Mac/Linux use "/etc/hosts"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts" 
REDIRECT = "127.0.0.1"

# Sites you want to block
WEBSITES = [
    "www.youtube.com", "youtube.com",
    "www.instagram.com", "instagram.com",
    "www.reddit.com", "reddit.com"
]

def block_sites():
    with open(HOSTS_PATH, "r+") as file:
        content = file.read()
        for site in WEBSITES:
            if site not in content:
                file.write(f"{REDIRECT} {site}\n")
    print("Sites Blocked!")

def unblock_sites():
    with open(HOSTS_PATH, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(site in line for site in WEBSITES):
                file.write(line)
        file.truncate()
    print("Sites Unblocked!")

def pomodoro():
    FOCUS = 25 * 60  # 25 minutes
    BREAK = 5 * 60   # 5 minutes
    
    while True:
        print("\nStarting 25min Focus Session...")
        block_sites()
        time.sleep(FOCUS)
        
        print("\nFocus over! 5min Break")
        unblock_sites()
        time.sleep(BREAK)
        
        again = input("Start another session? y/n: ")
        if again.lower() != "y":
            unblock_sites() # make sure sites are unblocked
            break

if __name__ == "__main__":
    print("Website Blocker Started. Run as Administrator!")
    pomodoro()