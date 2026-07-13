import re
import socket
import sys
from threading import Thread

# --- CONFIGURATION ---
WAF_HOST = "127.0.0.1"
WAF_PORT = 7777
BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8080  # Points to your custom web server or sandbox backend
BUFFER_SIZE = 8192

# --- SIGNATURE MATRIX (REGEX CORRELATION) ---
WAF_RULES = {
    "SQL Injection (SQLi)": re.compile(
        r"(union\s+select|select\s+.*\s+from|'\\\s*OR\s*['\"]?\d+['\"]?\s*=\s*['\"]?\d+|--|/\*|\*\/)", 
        re.IGNORECASE
    ),
    "Cross-Site Scripting (XSS)": re.compile(
        r"(<script.*?>|javascript:|onerror\s*=|onload\s*=|alert\s*\(|<img>)", 
        re.IGNORECASE
    ),
    "Directory Traversal": re.compile(
        r"(\.\./|\.\.\\|/etc/passwd|/windows/win\.ini)", 
        re.IGNORECASE
    )
}


def inspect_traffic(raw_http_payload: str) -> tuple[bool, str]:
    """Analyzes the raw text payload string for explicit threat signatures."""
    # Split the headers and content lines down to normalize inspection vectors
    for rule_name, regex_pattern in WAF_RULES.items():
        if regex_pattern.search(raw_http_payload):
            return True, rule_name
    return False, ""


def send_block_page(client_socket):
    """Dispatches a custom 403 Forbidden security block screen to the attacker."""
    body = (
        "<html><head><title>Access Denied</title></head>"
        "<body style='font-family:Arial,sans-serif; text-align:center; margin-top:100px; color:#cc0000;'>"
        "<h1>[!] Malicious Activity Detected</h1>"
        "<p>Your request has been intercepted and blocked by the Web Application Firewall (WAF).</p>"
        "</body></html>"
    )
    header = (
        "HTTP/1.1 403 Forbidden\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n\r\n"
    )
    client_socket.sendall((header + body).encode("utf-8"))


def handle_client(client_socket, client_address):
    """Intercepts, scans, and conditionally routes traffic streams."""
    print(f"\n[*] Intercepted pipeline stream from client: {client_address[0]}:{client_address[1]}")
    try:
        # 1. Read incoming stream request data
        request_bytes = client_socket.recv(BUFFER_SIZE)
        if not request_bytes:
            client_socket.close()
            return

        request_string = request_bytes.decode("utf-8", errors="ignore")

        # 2. Process inspection routine through WAF engine rules
        is_malicious, threat_type = inspect_traffic(request_string)

        if is_malicious:
            print(f"\033[91m[WAF BLOCK] Dropped request from {client_address[0]} due to: {threat_type}\033[0m")
            # Log the full request blocks to track the exploit payload signature
            with open("waf_security_alerts.log", "a") as f:
                f.write(f"Threat: {threat_type} | Source: {client_address[0]} \nPayload:\n{request_string}\n{'-'*60}\n")
            
            send_block_page(client_socket)
            client_socket.close()
            return

        print("[+] Request verified as clean. Routing upstream to backend server stack...")

        # 3. Establish upstream socket tunnel to the safe backend web server
        upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            upstream_socket.connect((BACKEND_HOST, BACKEND_PORT))
            upstream_socket.sendall(request_bytes)

            # Receive the response back from the real backend and proxy it to the client browser
            while True:
                response_bytes = upstream_socket.recv(BUFFER_SIZE)
                if len(response_bytes) > 0:
                    client_socket.sendall(response_bytes)
                else:
                    break
        except socket.error as e:
            print(f"[!] Unable to route to backend target application server: {e}")
            # Fallback error response
            err_body = "<h1>502 Bad Gateway</h1>"
            client_socket.sendall(f"HTTP/1.1 502 Bad Gateway\r\nContent-Length: {len(err_body)}\r\n\r\n{err_body}".encode())
        finally:
            upstream_socket.close()
            client_socket.close()

    except Exception as e:
        print(f"[!] Firewall connection proxy processing exception: {e}")
        client_socket.close()


def start_waf():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((WAF_HOST, WAF_PORT))
        server.listen(50)
        print("=" * 60)
        print(f"[+] WAF REVERSE PROXY running live at: http://{WAF_HOST}:{WAF_PORT}")
        print(f"[*] Upstream traffic will mirror onto backend structure: {BACKEND_HOST}:{BACKEND_PORT}")
        print("=" * 60)

        while True:
            client_sock, addr = server.accept()
            proxy_thread = Thread(target=handle_client, args=(client_sock, addr))
            proxy_thread.daemon = True
            proxy_thread.start()

    except KeyboardInterrupt:
        print("\n[-] Terminating firewall reverse proxy core modules.")
    finally:
        server.close()
        sys.exit(0)


if __name__ == "__main__":
    start_waf()
