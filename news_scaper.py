import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = "https://timesofindia.indiatimes.com/"

def scrape_news():
    print("Scraping news...")
    
    # Send request
    headers = {"User-Agent": "Mozilla/5.0"} # so website doesn't block us
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    
    # Find all headline tags. TOI uses 'span.w_tle' for main headlines
    for item in soup.find_all("span", class_="w_tle"):
        title = item.get_text().strip()
        link = item.find_parent("a")["href"] if item.find_parent("a") else ""
        full_link = "https://timesofindia.indiatimes.com" + link if link.startswith("/") else link
        
        if title: # avoid empty
            headlines.append({
                "Title": title,
                "Link": full_link,
                "Scraped At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    # Save to CSV
    df = pd.DataFrame(headlines)
    df.to_csv("news.csv", index=False, encoding="utf-8")
    
    print(f"Done! Scraped {len(df)} headlines")
    print(df.head(10)) # show first 10

if __name__ == "__main__":
    scrape_news()