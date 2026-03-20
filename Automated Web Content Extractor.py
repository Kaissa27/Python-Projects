import re 

def scrape_simulation():
    # Simulated HTML content (what you'd get from a website)
    web_content = """
    <html>
        <body>
            <div class='product'>
                <h2 class='title'>Ultra-Fast SSD</h2>
                <span class='price'>$120.00</span>
                <p class='desc'>High speed 1TB storage.</p>
            </div>
            <div class='product'>
                <h2 class='title'>DDR5 RAM</h2>
                <span class='price'>$85.50</span>
                <p class='desc'>16GB 5200MHz memory.</p>
            </div>
            <div class='product'>
                <h2 class='title'>Gaming Mouse</h2>
                <span class='price'>$45.99</span>
                <p class='desc'>RGB 12000 DPI sensor.</p>
            </div>
        </body>
    </html>
    """

    print("--- Automated Web Scraper Simulation ---")

    # 1. Extraction Phase (Regex)
    # We use Regular Expressions to find text between specific HTML tags
    titles = re.findall(r"<h2.*?>(.*?)</h2>", web_content)
    prices = re.findall(r"<span.*?>(.*?)</span>", web_content)

    # 2. Cleaning Phase
    # Strip '$' and convert to float for math operations
    numeric_prices = [float(p.replace('$', '')) for p in prices]

    # 3. Structuring Phase (Zip)
    # The 'zip' function pairs titles and prices into a list of tuples
    catalog = list(zip(titles, numeric_prices))

    # 4. Analysis & Reporting
    print(f"Scraped {len(catalog)} items from the page.\n")
    
    total_value = 0
    for item, price in catalog:
        print(f"Product: {item:<15} | Price: ${price:>7.2f}")
        total_value += price

    print("-" * 35)
    print(f"Total Catalog Value:   ${total_value:.2f}")

if __name__ == "__main__":
    scrape_simulation()