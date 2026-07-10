import datetime
import socket
import sys
from threading import Thread

# --- CONFIGURATION ---
BIND_IP = "0.0.0.0"  # Listen on all local interfaces
HONEYPORTS = {
    22: "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n",  # Fake SSH Banner
    23: "Welcome to Microsoft Telnet Service \r\nlogin: ",  # Fake Telnet Banner
    6379: "-ERR unknown command or authentication required\r\n"  # Fake Redis Response
}


def log_incident(client_ip, port, captured_data):
    """Structures and logs malicious interaction profiles to a file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ALERT: Connection on Honeyport {port} from IP: {client_ip}\n"
    
    if captured_data:
        # Sanitize data lines for visual logging cleanly
        clean_payload = captured_data.decode("utf-8", errors="ignore").strip()
        log_entry += f"   |_ Captured Payload String: {clean_payload}\n"
        
    print(f"\033[91m{log_entry}\033[0m")  # Print in red to emphasize the alert
    
    with open("honeypot_activity.log", "a") as log_file:
        log_file.write(log_entry + "-" * 50 + "\n")


def handle_intruder(client_socket, client_ip, port, banner):
    """Interacts with the scanning scanner to pull input signatures."""
    try:
        client_socket.settimeout(5.0)
        
        # 1. Dispatch deceptive banner profile immediately upon connection handshake
        if banner:
            client_socket.sendall(banner.encode("utf-8"))
            
        # 2. Capture incoming commands or automated fuzzing attempts
        data = client_socket.recv(1024)
        log_incident(client_ip, port, data)
        
    except socket.timeout:
        # Scanner connected to map the port open but did not send data down the channel
        log_incident(client_ip, port, b"[No Payload - Connection Timeout]")
    except Exception as e:
        print(f"[!] Error handling interaction sequence: {e}")
    finally:
        client_socket.close()


def start_honeyport_daemon(port, banner):
    """Maintains an individual socket listener loop for an allocated port profile."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        listener.bind((BIND_IP, port))
        listener.listen(10)
        
        while True:
            client_sock, client_addr = listener.accept()
            # Offload processing immediately to a dedicated handling worker thread
            worker = Thread(target=handle_intruder, args=(client_sock, client_addr[0], port, banner))
            worker.daemon = True
            worker.start()
            
    except Exception as e:
        print(f"[!] Fatal anomaly crashed socket daemon on port {port}: {e}")
    finally:
        listener.close()


def main():
    print("=" * 60)
    print("      ACTIVE MULTI-SERVICE HONEYPOT ENVIRONMENT       ")
    print("=" * 60)
    print(f"[*] Activating defensive decoys on IP reference target: {BIND_IP}")
    
    # Spawn a detached service tracker daemon for every configured port definition
    for port, banner in HONEYPORTS.items():
        print(f"[+] Launching monitoring wrapper on port: {port}")
        daemon_thread = Thread(target=start_honeyport_daemon, args=(port, banner))
        daemon_thread.daemon = True
        daemon_thread.start()
        
    print("=" * 60)
    print("[*] Decoys active. System monitoring lines live... Press Ctrl+C to stop.")
    
    try:
        # Keep main structural runtime alive while subprocess workers route data
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[-] Deactivating decoy profiles. Committing log registers down safely.")
        sys.exit(0)


if __name__ == "__main__":
    main()
