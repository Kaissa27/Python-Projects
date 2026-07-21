pip install dnspython


import sys
import dns.resolver

# --- CONFIGURATION ---
TARGET_DOMAIN = "example.com"

# Common subdomains wordlist simulation
MOCK_SUBDOMAINS = [
    "www",
    "mail",
    "remote",
    "blog",
    "webmail",
    "server",
    "ns1",
    "ns2",
    "smtp",
    "secure",
    "vpn",
    "api",
    "dev",
    "staging",
    "admin"
]


def enumerate_subdomains(domain, wordlist):
    """Queries DNS records for each prefix appended to the target root domain."""
    print("=" * 60)
    print(f"[*] Starting Subdomain Enumeration for: {domain}")
    print(f"[*] Testing {len(wordlist)} common subdomain prefixes...")
    print("=" * 60 + "\n")

    # Configure custom DNS resolver parameters
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1.5
    resolver.lifetime = 1.5

    discovered_assets = []

    for prefix in wordlist:
        subdomain = f"{prefix}.{domain}"
        
        try:
            # Query the 'A' record (IPv4 address mapping) for the target subdomain
            answers = resolver.resolve(subdomain, 'A')
            
            ip_addresses = [str(rdata) for rdata in answers]
            ip_str = ", ".join(ip_addresses)
            
            print(f"\033[92m[+] DISCOVERED: {subdomain} -> [{ip_str}]\033[0m")
            discovered_assets.append((subdomain, ip_addresses))

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            # NXDOMAIN means the domain name does not exist on the DNS server
            pass
        except dns.resolver.Timeout:
            print(f"[-] Query timed out for: {subdomain}")
        except Exception as e:
            # General fallback for unexpected DNS network errors
            pass

    # Summary Report
    print("\n" + "=" * 60)
    print("                  ENUMERATION SUMMARY REPORT                 ")
    print("=" * 60)
    print(f"[+] Total Active Subdomains Found: {len(discovered_assets)}")
    for sub, ips in discovered_assets:
        print(f"    |_ {sub:<30} -> {', '.join(ips)}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        enumerate_subdomains(TARGET_DOMAIN, MOCK_SUBDOMAINS)
    except KeyboardInterrupt:
        print("\n[-] Enumeration sequence stopped by user.")
        sys.exit(0)
