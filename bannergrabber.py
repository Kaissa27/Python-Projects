import concurrent.futures
import socket
import sys

# --- CONFIGURATION ---
TARGET_HOST = "scanme.nmap.org"  # Authorized public testing host by Nmap
PORTS_TO_SCAN = [21, 22, 25, 80, 110, 143, 443, 8080]
TIMEOUT_SECONDS = 2.0


def grab_banner(host, port):
    """Establishes a raw TCP socket connection and attempts to read service banners."""
    banner_info = None

    try:
        # Create an IPv4 TCP Socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT_SECONDS)
            
            # 1. Attempt TCP Three-Way Handshake
            result = s.connect_ex((host, port))
            
            if result == 0:  # Port is OPEN
                # Send a generic probe line to stimulate HTTP or standard service responses
                probe = b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n"
                
                try:
                    s.sendall(probe)
                    banner_bytes = s.recv(1024)
                    banner_info = banner_bytes.decode("utf-8", errors="ignore").strip().split("\n")[0]
                except socket.timeout:
                    banner_info = "Open (No initial banner broadcast)"

                return port, True, banner_info

    except Exception as e:
        pass

    return port, False, None


def run_port_scan():
    print("=" * 65)
    print("      NETWORK PORT SCANNER & SERVICE BANNER GRABBER         ")
    print("=" * 65)
    
    try:
        target_ip = socket.gethostbyname(TARGET_HOST)
    except socket.gaierror:
        print(f"\033[91m[!] Error: Unable to resolve hostname '{TARGET_HOST}'\033[0m")
        return

    print(f"[*] Target Hostname : {TARGET_HOST}")
    print(f"[*] Target Resolved : {target_ip}")
    print(f"[*] Auditing Ports  : {PORTS_TO_SCAN}")
    print("[*] Executing multi-threaded connection probes...\n")

    open_services = []

    # Use ThreadPoolExecutor for fast, concurrent socket scanning
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(grab_banner, target_ip, port) for port in PORTS_TO_SCAN]
        
        for future in concurrent.futures.as_completed(futures):
            port, is_open, banner = future.result()
            
            if is_open:
                open_services.append((port, banner))
                print(f"\033[92m[+] PORT {port:<5} [OPEN]\033[0m")
                print(f"    |_ Banner Metadata: '{banner}'")

    print("\n" + "=" * 65)
    print("                    SCAN AUDIT SUMMARY                        ")
    print("=" * 65)
    print(f"[+] Active Open Ports Discovered: {len(open_services)} / {len(PORTS_TO_SCAN)}")
    for port, banner in open_services:
        print(f"    |_ Port {port:<5} -> {banner}")
    print("=" * 65)


if __name__ == "__main__":
    try:
        run_port_scan()
    except KeyboardInterrupt:
        print("\n[-] Network audit canceled by user.")
        sys.exit(0)
