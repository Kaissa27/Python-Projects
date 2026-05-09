import requests
from bs4 import BeautifulSoup

def scrape_news():
    url = 'https://news.ycombinator.com/'
    
    # 1. Grab the webpage data
    headers = {'User-Agent': 'Mozilla/5.0'} # Pretend to be a browser
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # 2. Convert HTML into a searchable "Soup"
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Find all headline tags (on HN, they are in spans with class 'titleline')
        headlines = soup.find_all('span', class_='titleline')
        
        print(f"--- TOP HEADLINES FROM {url} ---")
        for i, line in enumerate(headlines[:10], 1):
            # Get the text and the link inside the span
            link = line.find('a')
            print(f"{i}. {link.text}")
            print(f"   Link: {link['href']}\n")
    else:
        print(f"Failed to reach site. Status code: {response.status_code}")

# scrape_news()
