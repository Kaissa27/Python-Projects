import datetime
import socket
import sys

# --- CONFIGURATION ---
BIND_HOST = "0.0.0.0"     # Listen on all local network interfaces
BIND_PORT = 2222          # Standard honeypot port (simulating SSH)
HONEYPOT_LOG = "honeypot_events.log"

# A fake service banner designed to make the decoy look like a real SSH service
FAKE_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.2\r\n"


def log_event(client_ip, client_port, payload_received):
    """Formats and appends connection details to a local security log."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"[{timestamp}] HONEYPOT ALERT!\n"
    log_entry += f"   |_ Source IP: {client_ip}:{client_port}\n"
    log_entry += f"   |_ Captured Input: {repr(payload_received)}\n"
    log_entry += "-" * 50 + "\n"

    # Display high-visibility red alert in the terminal
    print(f"\033[91m{log_entry.strip()}\033[0m\n")

    with open(HONEYPOT_LOG, "a") as log_file:
        log_file.write(log_entry)


def start_honeypot():
    print("=" * 60)
    print("           BASIC DECOY HONEYPOT LISTENER DAEMON           ")
    print("=" * 60)
    print(f"[*] Initializing listener on port {BIND_PORT}...")
    print(f"[*] Logging intruder metadata to: ./{HONEYPOT_LOG}")
    print("[*] Waiting for incoming unauthorized connections...\n")

    # 1. Establish the TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((BIND_HOST, BIND_PORT))
        server_socket.listen(5)

        while True:
            # 2. Accept incoming connection from an intruder or scanner
            client_socket, client_address = server_socket.accept()
            client_ip, client_port = client_address

            print(f"[!] Intrusion detected from {client_ip}:{client_port} — engaging trap...")

            try:
                # 3. Transmit the fake banner string
                client_socket.sendall(FAKE_BANNER.encode("utf-8"))

                # 4. Set a brief timeout to capture initial input payload (e.g., login attempts)
                client_socket.settimeout(3.0)
                captured_bytes = client_socket.recv(1024)
                
                payload = captured_bytes.decode("utf-8", errors="ignore").strip()

                # 5. Record the security incident
                log_event(client_ip, client_port, payload)

            except socket.timeout:
                # Intruder connected but didn't send data immediately
                log_event(client_ip, client_port, "<NO PAYLOAD / TIMEOUT>")
            except Exception as e:
                log_event(client_ip, client_port, f"<ERROR: {e}>")
            finally:
                client_socket.close()

    except Exception as err:
        print(f"[!] Critical Honeypot Error: {err}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    try:
        start_honeypot()
    except KeyboardInterrupt:
        print("\n[-] Honeypot daemon safely offline.")
        sys.exit(0)
