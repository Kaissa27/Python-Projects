import datetime
import socket
import ssl
import sys

# --- CONFIGURATION ---
TARGET_HOSTS = [
    ("example.com", 443),
    ("google.com", 443),
    ("expired.badssl.com", 443)  # Public test target for expired SSL certs
]

# Warning threshold in days for upcoming certificate expirations
EXPIRATION_WARN_DAYS = 30


def inspect_ssl_certificate(hostname, port=443):
    """Establishes a TLS connection to retrieve and validate an X.509 certificate."""
    print(f"[*] Connecting to {hostname}:{port} to retrieve SSL/TLS certificate...")
    
    # Create an SSL context configured to use system CA store
    context = ssl.create_default_context()

    try:
        # Establish a standard TCP socket connection
        with socket.create_connection((hostname, port), timeout=3.0) as sock:
            # Wrap the socket in a TLS layer and initiate the SSL handshake
            with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                # Extract the peer certificate metadata dictionary
                cert = ssl_sock.getpeercert()
                cipher = ssl_sock.cipher()
                protocol_version = ssl_sock.version()

                # Parse expiration date (Format: 'MMM DD HH:MM:SS YYYY GMT')
                not_after_str = cert['notAfter']
                expiry_date = datetime.datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
                now = datetime.datetime.utcnow()
                days_until_expiry = (expiry_date - now).days

                # Extract Common Name (CN) and Subject Alternative Names (SANs)
                subject = dict(x[0] for x in cert.get('subject', []))
                common_name = subject.get('commonName', 'N/A')

                print(f"\033[92m[+] SUCCESS: Established {protocol_version} Connection\033[0m")
                print(f"   |_ Issued To (CN) : {common_name}")
                print(f"   |_ Cipher Suite   : {cipher[0]} ({cipher[2]} bits)")
                print(f"   |_ Valid Until    : {expiry_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                
                # Evaluate Expiration Status
                if days_until_expiry < 0:
                    print(f"   |_ \033[91m[STATUS] EXPIRED! (Expired {abs(days_until_expiry)} days ago)\033[0m")
                elif days_until_expiry <= EXPIRATION_WARN_DAYS:
                    print(f"   |_ \033[93m[STATUS] WARNING: Expiring soon ({days_until_expiry} days remaining)\033[0m")
                else:
                    print(f"   |_ \033[92m[STATUS] HEALTHY ({days_until_expiry} days remaining)\033[0m")

    except ssl.SSLCertVerificationError as e:
        print(f"\033[91m[!] CERTIFICATE INVALID / TRUST FAILURE: {e.reason}\033[0m")
    except socket.timeout:
        print(f"\033[91m[!] CONNECTION TIMEOUT: Host {hostname}:{port} did not respond.\033[0m")
    except Exception as err:
        print(f"[!] Unable to complete TLS audit for {hostname}: {err}")
        
    print("-" * 60)


def run_ssl_audit():
    print("=" * 60)
    print("        BASIC TLS/SSL CERTIFICATE & EXPIRY AUDITOR        ")
    print("=" * 60)
    print(f"[*] Auditing {len(TARGET_HOSTS)} target host(s)...")
    print(f"[*] Expiration Alert Threshold: <= {EXPIRATION_WARN_DAYS} days\n")

    for host, port in TARGET_HOSTS:
        inspect_ssl_certificate(host, port)

    print("=" * 60)


if __name__ == "__main__":
    try:
        run_ssl_audit()
    except KeyboardInterrupt:
        print("\n[-] SSL audit sequence terminated by user.")
        sys.exit(0)
