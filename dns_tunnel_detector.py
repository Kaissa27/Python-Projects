from collections import Counter
import math
import re
import sys

# --- CONFIGURATION ---
# Subdomain entropy threshold (higher means more random, typical for base64/hex encoding)
ENTROPY_THRESHOLD = 3.8
# Maximum normal subdomain character length
MAX_SUBDOMAIN_LENGTH = 30

# Simulated DNS query log records
MOCK_DNS_LOGS = [
    "2026-07-30 10:00:01 | Client: 192.168.1.105 | Query: google.com",
    "2026-07-30 10:00:02 | Client: 192.168.1.105 | Query: api.github.com",
    "2026-07-30 10:00:05 | Client: 10.0.0.42     | Query: Q29uZmlkZW50aWFsRGF0YTIwMjY=.bad-actor.net",  # Base64 Exfiltration
    "2026-07-30 10:00:08 | Client: 192.168.1.110 | Query: mail.corp-internal.local",
    "2026-07-30 10:00:12 | Client: 10.0.0.42     | Query: 4a6f686e446f6553534e393938383737.bad-actor.net",  # Hex Exfiltration
    "2026-07-30 10:00:15 | Client: 192.168.1.105 | Query: updates.microsoft.com"
]


def calculate_shannon_entropy(data_str):
    """Calculates Shannon Entropy to measure randomness in string data."""
    if not data_str:
        return 0.0
    
    length = len(data_str)
    counts = Counter(data_str)
    entropy = 0.0

    for count in counts.values():
        p_x = count / length
        entropy -= p_x * math.log2(p_x)

    return round(entropy, 2)


def extract_subdomain(domain_name):
    """Isolates the prefix/subdomain portion of a FQDN."""
    parts = domain_name.strip().split(".")
    # If the domain has more than two labels (e.g., sub.example.com), extract the subdomain portion
    if len(parts) > 2:
        return ".".join(parts[:-2])
    return ""


def analyze_dns_traffic(dns_logs):
    print("=" * 70)
    print("       DNS DATA EXFILTRATION & TUNNELING DETECTION ENGINE       ")
    print("=" * 70)
    print(f"[*] Processing {len(dns_logs)} DNS lookup queries...")
    print(f"[*] Threat Policies: Entropy > {ENTROPY_THRESHOLD} | Max Subdomain Length > {MAX_SUBDOMAIN_LENGTH} chars\n")

    log_pattern = re.compile(
        r"^(?P<time>.*?)\s+\|\s+Client:\s+(?P<ip>[\d\.]+)\s+\|\s+Query:\s+(?P<query>[a-zA-Z0-9\.-]+)"
    )

    detected_alerts = 0

    for line in dns_logs:
        match = log_pattern.search(line)
        if match:
            ip = match.group("ip")
            query = match.group("query")
            subdomain = extract_subdomain(query)

            if not subdomain:
                continue

            # Calculate metrics on the extracted subdomain payload
            entropy = calculate_shannon_entropy(subdomain)
            sub_len = len(subdomain)

            is_high_entropy = entropy >= ENTROPY_THRESHOLD
            is_oversized = sub_len >= MAX_SUBDOMAIN_LENGTH

            if is_high_entropy or is_oversized:
                detected_alerts += 1
                print(f"\033[91m[CRITICAL ALERT] SUSPECTED DNS TUNNELING / EXFILTRATION")
                print(f"   |_ Client IP   : {ip}")
                print(f"   |_ Full Query  : {query}")
                print(f"   |_ Subdomain   : {subdomain}")
                print(f"   |_ Payload Len : {sub_len} chars (Oversized: {is_oversized})")
                print(f"   |_ Entropy     : {entropy} / 8.0 (High Randomness: {is_high_entropy})\033[0m\n")
            else:
                print(f"\033[92m[+] Safe Query: {query:<30} | Subdomain Entropy: {entropy}\033[0m")

    print("=" * 70)
    print("                    ANALYSIS SUMMARY REPORT                   ")
    print("=" * 70)
    print(f"[+] Total Queries Audited  : {len(dns_logs)}")
    if detected_alerts > 0:
        print(f"\033[91m[!] WARNING: Flagged {detected_alerts} potential DNS data exfiltration attempt(s)!\033[0m")
    else:
        print("\033[92m[+] CLEAN: No DNS tunneling signatures detected.\033[0m")
    print("=" * 70)


if __name__ == "__main__":
    try:
        analyze_dns_traffic(MOCK_DNS_LOGS)
    except KeyboardInterrupt:
        print("\n[-] DNS monitoring stopped.")
        sys.exit(0)
