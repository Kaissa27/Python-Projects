pip install requests


import os
import sys
import requests

# --- CONFIGURATION ---
# Replace with a sandbox target environment (e.g., http://localhost:8080 or a safe testing domain)
TARGET_URL = "http://example.com" 

# A quick mock list representing an external "wordlist" file of directories to test
MOCK_WORDLIST = [
    "admin",
    "login",
    "secret",
    "backup.zip",
    "wp-admin",
    "config.php",
    "api/v1",
    "images",
    "hidden-portal"
]


def run_directory_scan():
    # Clean up trailing slashes from the target URL to ensure clean formatting
    base_url = TARGET_URL.rstrip("/")
    
    print("=" * 60)
    print(f"[*] Initializing Directory Brute-Forcer against: {base_url}")
    print(f"[*] Testing {len(MOCK_WORDLIST)} common paths against the web server...")
    print("=" * 60 + "\n")

    discovered_paths = []

    for path in MOCK_WORDLIST:
        # Construct the complete target endpoint
        full_target_url = f"{base_url}/{path}"
        
        try:
            # Send a fast GET request. We set allow_redirects=False to spot true 301/302 redirects
            response = requests.get(full_target_url, timeout=2.0, allow_redirects=False)
            status_code = response.status_code

            # Interpret the standard HTTP status code definitions
            if status_code == 200:
                print(f"\033[92m[+] FOUND (200 OK): {full_target_url}\033[0m")
                discovered_paths.append((full_target_url, "200 OK"))
            elif status_code in [301, 302]:
                print(f"\033[93m[*] REDIRECT ({status_code}): {full_target_url} -> {response.headers.get('Location')}\033[0m")
                discovered_paths.append((full_target_url, f"Redirect {status_code}"))
            elif status_code == 403:
                print(f"\033[91m[!] FORBIDDEN (403): {full_target_url} (Path exists but is restricted)\033[0m")
                discovered_paths.append((full_target_url, "403 Forbidden"))
            else:
                # 404 Not Found or other codes — skip printing to keep output clean
                pass

        except requests.RequestException as e:
            print(f"[!] Connection error while testing {full_target_url}: {e}")
            continue

    # Summary Report
    print("\n" + "=" * 60)
    print("                    SCANNING REPORT                   ")
    print("=" * 60)
    print(f"[+] Total Discovered Endpoints: {len(discovered_paths)}")
    for url, status in discovered_paths:
        print(f"    |_ [{status}] {url}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_directory_scan()
    except KeyboardInterrupt:
        print("\n[-] Scan sequence cancelled by user request.")
        sys.exit(0)
