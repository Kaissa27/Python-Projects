from concurrent.futures import ThreadPoolExecutor
import socket
import sys

# --- CONFIGURATION ---
TARGET_HOST = "localhost"  # Can be changed to a target IP or domain
PORT_RANGE = range(1, 1025)  # Scan the well-known ports (1 to 1024)
TIMEOUT = 1.5  # Seconds to wait for a connection response


def banner_grab(sock):
    """Attempts to read the initial welcome banner from an open port."""
    try:
        # Send a generic request string to prompt a response if the protocol requires it
        sock.sendall(b"Hello\r\n")
        banner = sock.recv(1024)
        if banner:
            # Decode bytes safely, replacing unprintable characters
            return banner.decode("utf-8", errors="ignore").strip()
    except socket.error:
        # If the service doesn't send a banner or times out, return a fallback notice
        return "No banner responded (Service active but silent)"
    return "Unknown Service"


def scan_port(port):
    """Checks if a specific port is open and grabs its service metadata."""
    # Establish an IPv4 (AF_INET) TCP (SOCK_STREAM) socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)

        # connect_ex returns 0 if the connection operation succeeded
        result = s.connect_ex((TARGET_HOST, port))

        if result == 0:
            print(f"[+] Port {port} is OPEN")
            banner = banner_grab(s)
            print(f"    |_ Banner Metadata: {banner}")
            return {"port": port, "status": "Open", "banner": banner}

    return None


def run_scanner():
    print("=" * 50)
    print(f"[*] Starting Multithreaded Scan on Host: {TARGET_HOST}")
    print(f"[*] Scanning Ports: {PORT_RANGE.start} through {PORT_RANGE.stop - 1}")
    print("=" * 50)

    open_ports_discovered = []

    # Use a ThreadPoolExecutor to run connection checks concurrently
    # max_workers caps the simultaneous threads to maintain system stability
    with ThreadPoolExecutor(max_workers=100) as executor:
        # Map the scan_port function across our entire target range
        results = executor.map(scan_port, PORT_RANGE)

        for res in results:
            if res:
                open_ports_discovered.append(res)

    print("\n" + "=" * 50)
    print("[*] Scan completed.")
    print(f"[+] Total Open Ports Identified: {len(open_ports_discovered)}")
    print("=" * 50)


if __name__ == "__main__":
    try:
        run_scanner()
    except KeyboardInterrupt:
        print("\n[!] Scan aborted by user control.")
        sys.exit()
