import socket
import sys
import time

# --- CONFIGURATION ---
TARGET_HOST = "127.0.0.1"  # Localhost for safe, local environment testing

# The secret combination sequence of closed ports (the secret knock)
SECRET_KNOCK_SEQUENCE = [7000, 8500, 9900]

# The protected port that will "open" only after a successful knock sequence
TARGET_PROTECTED_PORT = 22


def transmit_single_knock(host, port):
    """Sends a fast TCP connection attempt to act as a knock signal."""
    try:
        # Initialize a basic TCP network socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a very short timeout since we expect the port to be closed or drop packets
        s.settimeout(0.5)
        
        # Connect to generate the network packet sequence
        s.connect((host, port))
        s.close()
    except Exception:
        # We expect a connection failure/refusal on closed ports; 
        # the network packet itself is what the firewall or knocking daemon tracks.
        pass


def execute_knocking_sequence():
    print("=" * 60)
    print(f"[*] INITIALIZING PORT-KNOCKING ROUTINE AGAINST: {TARGET_HOST}")
    print("=" * 60)

    # Step 1: Execute the knocking sequence loop
    for i, port in enumerate(SECRET_KNOCK_SEQUENCE, 1):
        print(f"[*] Transmitting Knock #{i} to Target Port: {port}...")
        transmit_single_knock(TARGET_HOST, port)
        
        # Introduce a brief delay between transmission sequences to prevent overlapping
        time.sleep(0.3)

    print("\n[+] Secret knocking sequence completed successfully.")
    print(f"[*] Attempting connection hook onto protected service port: {TARGET_PROTECTED_PORT}...")
    print("-" * 60)

    # Step 2: Attempt to reach the now supposedly "unlocked" target port
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(2.0)
        
        # Connect to verify if the port is accessible
        result = test_socket.connect_ex((TARGET_HOST, TARGET_PROTECTED_PORT))
        
        if result == 0:
            print(f"\033[92m[SUCCESS] Port {TARGET_PROTECTED_PORT} IS OPEN! Knock authentication validated.\033[0m")
        else:
            print(f"\033[91m[-] Connection Refused (Code {result}). Protected port remains locked.\033[0m")
            print("[*] Note: In a real architecture, a backend daemon listening to traffic logs handles the firewall updates.")
            
        test_socket.close()

    except Exception as e:
        print(f"[!] Target verification processing anomaly: {e}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        execute_knocking_sequence()
    except KeyboardInterrupt:
        print("\n[-] Sequence cancelled.")
        sys.exit(0)
