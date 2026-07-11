pip install requests beautifulsoup4

from collections import deque
import re
import sys
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

# --- CONFIGURATION ---
# Replace with a locally hosted sandbox environment (e.g., DVWA or OWASP Juice Shop)
# DO NOT scan unauthorized external web properties.
START_URL = "http://example.com"  
MAX_PAGES_TO_CRAWL = 15
TIMEOUT = 3.0

# Mock local vulnerability database matching software signatures to CVE summaries
VULNERABILITY_FEED = {
    "wordpress 5.4": "CVE-2020-1147: Authenticated Cross-Site Scripting (XSS) in Customizer",
    "jquery 1.12.4": "CVE-2016-10707: Denial of Service (DoS) vulnerability via parsing manipulation",
    "bootstrap 3.3.7": "CVE-2018-14041: Cross-Site Scripting (XSS) via data-target attribute",
    "joomla 3.9.0": "CVE-2019-10651: Arbitrary File Upload via Core Media Component"
}


def extract_links(soup, base_url):
    """Parses HTML anchor tags to find internal URLs belonging to the target site."""
    found_links = set()
    parsed_base = urlparse(base_url)

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        # Resolve relative links (e.g., /about.html -> http://example.com/about.html)
        full_url = urljoin(base_url, href)
        parsed_full = urlparse(full_url)

        # Ensure the spider doesn't drift away to external third-party domains
        if parsed_full.netloc == parsed_base.netloc:
            # Strip anchors/fragments (#section1) to avoid duplicate crawling
            sanitized_url = full_url.split("#")[0]
            found_links.add(sanitized_url)

    return found_links


def audit_page_components(soup, url):
    """Inspects page elements, generator tags, and scripts for software footprints."""
    signatures_discovered = set()

    # 1. Inspect HTML <meta> tags (frequently used by CMS platforms like WordPress/Joomla)
    meta_generator = soup.find("meta", attrs={"name": "generator"})
    if meta_generator and meta_generator.get("content"):
        signatures_discovered.add(meta_generator["content"].strip().lower())

    # 2. Inspect script tags tracking popular JS library paths
    for script in soup.find_all("script", src=True):
        src_path = script["src"].lower()
        # Use Regex patterns to extract basic library names and versions
        match = re.search(r"(jquery|bootstrap|angular|vue)[\-\/]?([\d\.]+)?", src_path)
        if match:
            lib_name = match.group(1)
            version = match.group(2) if match.group(2) else "unknown"
            signatures_discovered.add(f"{lib_name} {version}")

    # 3. Correlate found versions with the Vulnerability Feed
    if signatures_discovered:
        print(f"[*] Software signatures identified on page: {url}")
        for sig in signatures_discovered:
            print(f"   |_ Detected: {sig}")
            # Check for direct matches or partial string signatures
            for flaw_key, details in VULNERABILITY_FEED.items():
                if flaw_key in sig:
                    print(f"\033[91m   [!] VULNERABILITY MATCH: {details}\033[0m")


def run_spider():
    print("=" * 60)
    print(f"[*] Launching Active Vulnerability Spider on: {START_URL}")
    print("=" * 60)

    # Use a double-ended queue (deque) to manage the Breadth-First Search (BFS) crawl
    queue = deque([START_URL])
    visited_urls = set()

    while queue and len(visited_urls) < MAX_PAGES_TO_CRAWL:
        current_url = queue.popleft()

        if current_url in visited_urls:
            continue

        print(f"\n[*] Mapping Request -> {current_url}")
        try:
            response = requests.get(current_url, timeout=TIMEOUT)
            visited_urls.add(current_url)

            # Ensure we are analyzing HTML text content, not binary assets or downloads
            if "text/html" not in response.headers.get("Content-Type", ""):
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Execute the passive vulnerability inspection logic
            audit_page_components(soup, current_url)

            # Discover and queue next pipeline URLs
            discovered_links = extract_links(soup, current_url)
            for link in discovered_links:
                if link not in visited_urls and link not in queue:
                    queue.append(link)

        except requests.RequestException as e:
            print(f"[!] Request transmission failed on {current_url}: {e}")
            visited_urls.add(current_url)

    print("\n" + "=" * 60)
    print(f"[*] Crawl complete. Total internal pages audited: {len(visited_urls)}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_spider()
    except KeyboardInterrupt:
        print("\n[-] Crawl routine terminated by user command.")
        sys.exit(0)
