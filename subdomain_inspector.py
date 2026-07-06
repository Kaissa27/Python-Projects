pip install requests

from concurrent.futures import ThreadPoolExecutor
import socket
import sys
import requests

# --- CONFIGURATION ---
TARGET_DOMAIN = "google.com"  # Replace with your authorized target domain
THREADS = 20
TIMEOUT = 3.0

# A small common wordlist boilerplate for demo purposes
# In real scenarios, you would read a large wordlist file (e.g., subdomains-top1mil.txt)
MOCK_WORDLIST = [
    "www", "mail", "remote", "blog", "webmail", "server", "ns1", "ns2",
    "smtp", "vpn", "secure", "dev", "staging", "test", "admin", "api"
]

# Standard HTTP headers often exposing underlying technology stack signatures
INTERESTING_HEADERS = ["Server", "X-Powered-By", "X-AspNet-Version", "X-Runtime", "Via"]


def inspect_subdomain_http(subdomain_url):
    """Establishes an HTTP request to analyze server header banners."""
    try:
        # Perform request without following redirects to see the initial server shield
        response = requests.get(f"http://{subdomain_url}", timeout=TIMEOUT, allow_redirects=False)
        print(f"[+] Active Web App Found: http://{subdomain_url} (Status: {response.status_code})")
        
        # Look for explicit infrastructure banners
        found_banners = []
        for header in INTERESTING_HEADERS:
            if header in response.headers:
                found_banners.append(f"{header}: {response.headers[header]}")
        
        if found_banners:
            for banner in found_banners:
                print(f"    |_ Banner Signature -> {banner}")
        else:
            print("    |_ Banner Signature -> Generic/Hidden headers")
            
    except requests.RequestException:
        # Subdomain resolves via DNS but doesn't have an active web port listening
        print(f"[!] Active DNS Found: {subdomain_url} (No active HTTP service response)")


def check_subdomain(sub_word):
    """Performs a low-level DNS query resolution string to verify subdomain existence."""
    full_subdomain = f"{sub_word}.{TARGET_DOMAIN}"
    try:
        # Use low-level socket API to see if the host resolves an IP
        socket.gethostbyname(full_subdomain)
        # If it doesn't throw an exception, the host exists!
        inspect_subdomain_http(full_subdomain)
    except socket.gaierror:
        # Host name not found/resolved
        pass


def run_enumeration():
    print("=" * 60)
    print(f"[*] Starting Subdomain Enumeration on: {TARGET_DOMAIN}")
    print(f"[*] Thread Worker Allocation Pool: {THREADS}")
    print("=" * 60)

    # Use a ThreadPoolExecutor to run connection checks concurrently
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(check_subdomain, MOCK_WORDLIST)

    print("\n" + "=" * 60)
    print("[*] Enumeration mapping complete.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_enumeration()
    except KeyboardInterrupt:
        print("\n[-] Enumeration sequence stopped by user control.")
        sys.exit(0)
