import html
import re
import sys
import urllib.parse

# --- DEFENSIVE RULE MATCHING SIGNATURES ---
# Regular expressions designed to catch common injection vectors
INJECTION_SIGNATURES = {
    "SQL Injection (SQLi)": [
        r"(?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|UNION|EXEC)\b",
        r"(?i)OR\s+['\"]?1['\"]?\s*=\s*['\"]?1",
        r"--\s*$",
        r"/\*.*?\*/"
    ],
    "Cross-Site Scripting (XSS)": [
        r"(?i)<script.*?>.*?</script>",
        r"(?i)javascript\s*:",
        r"(?i)onload\s*=",
        r"(?i)<iframe.*?>",
        r"(?i)onerror\s*="
    ],
    "Directory Traversal": [
        r"\.\./\.\./",
        r"\.\.\\\.\.\\",
        r"/etc/passwd",
        r"(?i)c:\\windows\\system32"
    ]
}


def inspect_and_sanitize_payload(raw_input_data):
    """Parses, inspects, and sanitizes incoming user input string."""
    print(f"[*] Raw Received Input: '{raw_input_data}'")

    # 1. Decode URL-encoded characters (e.g., %27 -> ', %3C -> <) to expose obfuscated inputs
    decoded_payload = urllib.parse.unquote(raw_input_data)
    
    threats_detected = []

    # 2. Match against known attack signature patterns
    for threat_type, patterns in INJECTION_SIGNATURES.items():
        for pattern in patterns:
            if re.search(pattern, decoded_payload):
                threats_detected.append(threat_type)
                break  # Move to next threat type once matched

    # 3. Handle results based on threat detection
    if threats_detected:
        print(f"\033[91m[WAF BLOCK 403] Threat Detected! Request Rejected.\033[0m")
        print(f"   |_ Violations: {', '.join(threats_detected)}")
        
        # 4. Perform Input Sanitization (stripping dangerous characters and HTML-encoding special symbols)
        sanitized_output = html.escape(decoded_payload)
        # Strip out direct script execution constructs safely
        sanitized_output = re.sub(r"(?i)<script.*?>.*?</script>", "[REMOVED_SCRIPT]", sanitized_output)
        
        print(f"   |_ Safe Sanitized Fallback: '{sanitized_output}'\n")
        return False, sanitized_output
    else:
        print("\033[92m[WAF ALLOW 200] Request Clean. Forwarding to Application Handler.\033[0m\n")
        return True, decoded_payload


def run_waf_simulation():
    print("=" * 65)
    print("      BASIC WEB APPLICATION FIREWALL (WAF) MIDDLEWARE       ")
    print("=" * 65)
    print("[*] Initializing signature rules database...")
    print("[*] Processing sample incoming HTTP GET/POST payload strings...\n")

    # Simulated incoming HTTP parameter inputs (mix of safe and malicious traffic)
    test_http_payloads = [
        "john_doe_99",                                                # Safe input
        "admin' OR '1'='1",                                           # SQL Injection attempt
        "<script>alert('Session Stolen!')</script>",                 # XSS attempt
        "%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E",           # URL-encoded XSS attempt
        "../../etc/passwd",                                           # Path Traversal attempt
        "user_id=105&category=books"                                 # Safe query string
    ]

    blocked_count = 0
    allowed_count = 0

    for payload in test_http_payloads:
        is_allowed, _ = inspect_and_sanitize_payload(payload)
        if is_allowed:
            allowed_count += 1
        else:
            blocked_count += 1

    print("=" * 65)
    print("                   WAF SIMULATION SUMMARY                     ")
    print("=" * 65)
    print(f"[+] Total HTTP Payloads Evaluated : {len(test_http_payloads)}")
    print(f"\033[92m[+] Allowed Requests (200 OK)    : {allowed_count}\033[0m")
    print(f"\033[91m[!] Blocked Requests (403 Forbidden): {blocked_count}\033[0m")
    print("=" * 65)


if __name__ == "__main__":
    try:
        run_waf_simulation()
    except KeyboardInterrupt:
        print("\n[-] WAF middleware simulation terminated.")
        sys.exit(0)
