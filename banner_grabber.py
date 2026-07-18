import socket
import sys

# --- CONFIGURATION ---
TARGET_HOST = "127.0.0.1"  # Localhost for safe, isolated testing
TARGET_PORTS = [21, 22, 25, 80, 110, 143, 443, 8080]  # Standard banner ports


def grab_banner(host, port):
    """Attempts to connect to a port and retrieve its raw service banner."""
    try:
        # 1. Initialize a TCP network socket socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 2. Set an aggressive timeout so the script doesn't hang on silent services
        s.settimeout(2.0)
        
        # 3. Establish the TCP connection handshake
        s.connect((host, port))
        
        # 4. Handle HTTP vs standard raw-text banners
        if port in [80, 8080]:
            # Web servers are silent until spoken to; we must send a basic HTTP request first
            http_request = "HEAD / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(host)
            s.sendall(http_request.encode('utf-8'))
            
        # 5. Read the incoming response buffer bytes
        raw_banner = s.recv(1024)
        s.close()
        
        # Decode the raw network bytes into readable text, ignoring unprintable artifacts
        return raw_banner.decode('utf-8', errors='ignore').strip()

    except socket.timeout:
        # Connected successfully, but the port didn't send data within the time limit
        s.close()
        return "[+] Port open but silent (Timeout)"
    except (ConnectionRefusedError, TimeoutError):
        # The port is completely closed or blocked by a local firewall
        return None
    except Exception as e:
        return f"[!] Connection error: {e}"


def run_enumeration():
    print("=" * 60)
    print(f"[*] Commencing Banner Grabbing Sequence on Target: {TARGET_HOST}")
    print("[*] Inspecting ports for application version indicators...")
    print("=" * 60 + "\n")

    discovered_services = 0

    for port in TARGET_PORTS:
        # Execute the grabber routine for each port
        banner = grab_banner(TARGET_HOST, port)
        
        if banner:
            discovered_services += 1
            print(f"\033[92m[+] SERVICE IDENTIFIED ON PORT {port}:\033[0m")
            # Indent the banner strings to display them cleanly in a sub-block layout
            indented_banner = "\n".join([f"    | {line}" for line in banner.splitlines()[:5]]) # Cap at 5 lines
            print(indented_banner)
            print("-" * 45)

    print("\n" + "=" * 60)
    print(f"[*] Enumeration finished. Identified {discovered_services} active application services.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_enumeration()
    except KeyboardInterrupt:
        print("\n[-] Enumeration routine aborted by user.")
        sys.exit(0)
