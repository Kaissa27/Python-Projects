import socket
import struct
import sys

def parse_ipv4_header(raw_data):
    """Parses the first 20 bytes of an IP packet to extract protocol details and addresses."""
    # The IPv4 header takes up the first 20 bytes of the packet
    ip_header_raw = raw_data[:20]
    
    # struct.unpack unpacks binary data into readable Python variables
    # '!BBHHHBBH4s4s' maps out the standard structural alignment format of an IP header
    unpacked_header = struct.unpack('!BBHHHBBH4s4s', ip_header_raw)
    
    # Extract protocol identifier flag (e.g., 6 = TCP, 17 = UDP, 1 = ICMP)
    protocol_type = unpacked_header[6]
    
    # Extract binary address spaces and convert them to readable string notation
    src_ip = socket.inet_ntoa(unpacked_header[8])
    dest_ip = socket.inet_ntoa(unpacked_header[9])
    
    return protocol_type, src_ip, dest_ip


def start_sniffer():
    print("=" * 60)
    print("         BASIC PRIVILEGED NETWORK PACKET SNIFFER        ")
    print("=" * 60)
    print("[*] Initializing raw network socket listener...")

    try:
        # Create a raw socket descriptor to capture internet protocol packets
        if sys.platform == "win32":
            # Windows structural specification variant
            sniffer_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            sniffer_socket.bind(("0.0.0.0", 0))
            # Include IP headers in the captured buffer stream
            sniffer_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            # Enable promiscuous mode to capture all traffic passing through the interface
            sniffer_socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        else:
            # Linux / macOS structural variant
            sniffer_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

        print("[SUCCESS] Raw socket interface active. Listening for packets...\n")

        packet_count = 0
        while packet_count < 10:  # Capture a small sample burst of 10 packets
            # Read 65535 bytes from the active network pipeline
            raw_packet, address_meta = sniffer_socket.recvfrom(65535)
            packet_count += 1

            # Process the raw bytes through our header parser routine
            proto, source, destination = parse_ipv4_header(raw_packet)

            # Map the protocol number to a readable string descriptor
            proto_name = "UNKNOWN"
            if proto == 6:
                proto_name = "TCP"
            elif proto == 17:
                proto_name = "UDP"
            elif proto == 1:
                proto_name = "ICMP"

            print(f"[PACKET #{packet_count}] Protocol: {proto_name} | Source: {source} -> Destination: {destination}")

        # Cleanup environment configurations if running on Windows
        if sys.platform == "win32":
            sniffer_socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

        print("\n[*] Sample packet trace quota met successfully.")
        print("=" * 60)

    except PermissionError:
        print("\n\033[91m[!] CRITICAL ERROR: Insufficient system privileges.")
        print("    |_ Raw socket creation failed. Please re-run this script as root/administrator.\033[0m\n")
    except Exception as e:
        print(f"[!] Initialization error: {e}")


if __name__ == "__main__":
    try:
        start_sniffer()
    except KeyboardInterrupt:
        print("\n[-] Sniffer deactivated by user input.")
        sys.exit(0)
