from concurrent.futures import ThreadPoolExecutor
import socket
import sys
import time

# --- CONFIGURATION ---
TARGET_HOST = "scanme.nmap.org"  # Authorized public test target provided by Nmap
PORTS_TO_SCAN = [21, 22, 25, 80, 110, 143, 443, 3306, 8080]
TIMEOUT = 2.0


def grab_banner(target, port):
    """Attempts to retrieve the service banner string from an open port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((target, port))

            # Send a generic HTTP probe for web ports, or wait passively for interactive banners (FTP/SSH/SMTP)
            if port in [80, 8080]:
                s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")

            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            # Clean up line breaks for single-line display
            return banner.replace("\r", " ").replace("\n", " ")
    except Exception:
        return "No banner returned / Silent service"


def scan_port(target_ip, port):
    """Attempts a TCP SYN/Connect probe against a specific port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            result = s.connect_ex((target_ip, port))

            # connect_ex returns 0 on successful TCP handshake
            if result == 0:
                banner = grab_banner(target_ip, port)
                return port, True, banner
    except Exception:
        pass
    
    return port, False, ""


def run_scanner(target):
    print("=" * 65)
    print("      NETWORK PORT SCANNER & SERVICE VERSION ENUMERATOR       ")
    print("=" * 65)

    try:
        target_ip = socket.gethostbyname(target)
        print(f"[*] Target Hostname : {target}")
        print(f"[*] Resolved IP     : {target_ip}")
        print(f"[*] Scanning Ports  : {PORTS_TO_SCAN}")
        print("[*] Initiating multi-threaded TCP handshake probes...\n")
    except socket.gaierror:
        print(f"\033[91m[!] Error: Hostname '{target}' could not be resolved.\033[0m")
        return

    start_time = time.time()
    open_ports = []

    # Use ThreadPoolExecutor to run port probes concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scan_port, target_ip, port) for port in PORTS_TO_SCAN]
        
        for future in futures:
            port, is_open, banner = future.result()
            if is_open:
                open_ports.append((port, banner))
                print(f"\033[92m[+] PORT {port:<5} OPEN\033[0m")
                print(f"    |_ Banner Response: {banner[:70]}")

    elapsed_time = round(time.time() - start_time, 2)

    print("\n" + "=" * 65)
    print("                    SCAN SUMMARY REPORT                       ")
    print("=" * 65)
    print(f"[+] Total Ports Scanned : {len(PORTS_TO_SCAN)}")
    print(f"[+] Open Ports Found   : {len(open_ports)}")
    print(f"[+] Scan Duration       : {elapsed_time} seconds")
    
    if open_ports:
        print("\n[*] Discovered Open Services:")
        for port, banner in open_ports:
            print(f"    |_ Port {port:<5} -> {banner[:50]}")
    print("=" * 65)


if __name__ == "__main__": 
    try:
        run_scanner(TARGET_HOST)
    except KeyboardInterrupt:
        print("\n[-] Port scan canceled by user.")
        sys.exit(0)
