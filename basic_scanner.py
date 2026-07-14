import socket
import sys

# --- CONFIGURATION ---
# '127.0.0.1' points to your local machine (localhost) for safe testing
TARGET_HOST = "127.0.0.1"

# A small list of common ports to test:
# 22 (SSH), 80 (HTTP Web), 443 (HTTPS Secure Web)
PORTS_TO_SCAN = [22, 80, 443, 8080]


def run_basic_scan():
    print("=" * 50)
    print(f"[*] Launching Basic Scan on Target Host: {TARGET_HOST}")
    print("=" * 50)

    for port in PORTS_TO_SCAN:
        print(f"[*] Testing port {port}...")

        # 1. Create a socket object
        # AF_INET specifies IPv4; SOCK_STREAM specifies TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2. Set a brief timeout so the script doesn't hang indefinitely
        s.settimeout(1.0)

        # 3. Attempt the network connection handshake
        # connect_ex returns an error code integer instead of throwing an exception
        result = s.connect_ex((TARGET_HOST, port))

        # 4. Evaluate the connection response status
        if result == 0:
            print(f"    [+] PORT {port} IS OPEN!")
        else:
            print(f"    [-] Port {port} is closed or filtered. (Code: {result})")

        # 5. Always close the socket descriptor when finished with the check
        s.close()

    print("\n[*] Scan process finalized successfully.")
    print("=" * 50)


if __name__ == "__main__":
    try:
        run_basic_scan()
    except KeyboardInterrupt:
        print("\n[!] Exiting scan sequence.")
        sys.exit(0)
