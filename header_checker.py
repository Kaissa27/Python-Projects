pip install requests


import sys
import requests

# --- CONFIGURATION ---
TARGET_URL = "https://example.com"

# Essential security headers and their operational purpose
SECURITY_HEADERS = {
    "Strict-Transport-Security": "Forces HTTPS connections (HSTS)",
    "Content-Security-Policy": "Prevents XSS and unauthorized script execution",
    "X-Frame-Options": "Protects against Clickjacking attacks",
    "X-Content-Type-Options": "Prevents MIME-type sniffing",
    "Referrer-Policy": "Controls how much referrer information is passed",
    "Permissions-Policy": "Restricts browser features (camera, mic, location)"
}


def audit_security_headers(url):
    """Sends a GET request and evaluates response headers and cookies for security flags."""
    print("=" * 60)
    print(f"[*] Starting Security Header Audit on: {url}")
    print("=" * 60 + "\n")

    try:
        response = requests.get(url, timeout=5.0)
        headers = response.headers
        cookies = response.cookies

        # 1. Evaluate Security Headers
        print("[+] HTTP RESPONSE HEADER ANALYSIS")
        print("-" * 60)
        
        missing_headers = 0
        for header, description in SECURITY_HEADERS.items():
            if header in headers:
                print(f"\033[92m[PRESENT] {header}\033[0m")
                print(f"          |_ Value: {headers[header][:60]}...")
            else:
                missing_headers += 1
                print(f"\033[91m[MISSING] {header}\033[0m")
                print(f"          |_ Purpose: {description}")

        # 2. Evaluate Cookie Security Flags
        print("\n[+] COOKIE SECURITY FLAG ANALYSIS")
        print("-" * 60)

        if not cookies:
            print("[*] No cookies set by the target application.")
        else:
            for cookie in cookies:
                print(f"[*] Cookie Name: {cookie.name}")
                
                # Check for HttpOnly flag (prevents JavaScript access to cookies)
                if cookie.has_nonstandard_attr('HttpOnly') or cookie.rest.get('HttpOnly'):
                    print("    |_ HttpOnly: \033[92mSecure\033[0m")
                else:
                    print("    |_ HttpOnly: \033[91mMissing (Vulnerable to XSS theft)\033[0m")

                # Check for Secure flag (ensures cookie is only sent over HTTPS)
                if cookie.secure:
                    print("    |_ Secure:   \033[92mSecure\033[0m")
                else:
                    print("    |_ Secure:   \033[91mMissing (Vulnerable to interception)\033[0m")

        # Summary Audit Results
        print("\n" + "=" * 60)
        print("                   AUDIT SUMMARY REPORT                   ")
        print("=" * 60)
        total_headers = len(SECURITY_HEADERS)
        present_headers = total_headers - missing_headers
        
        print(f"[+] Score: {present_headers}/{total_headers} Recommended Headers Implemented")
        if missing_headers == 0:
            print("\033[92m[RATING] EXCELLENT: Target demonstrates strong HTTP header hardening.\033[0m")
        else:
            print(f"\033[93m[RATING] NEEDS IMPROVEMENT: {missing_headers} critical headers missing.\033[0m")
        print("=" * 60)

    except requests.RequestException as e:
        print(f"[!] Target connection failed: {e}")


if __name__ == "__main__":
    try:
        audit_security_headers(TARGET_URL)
    except KeyboardInterrupt:
        print("\n[-] Audit canceled by user.")
        sys.exit(0)
