import socket
import struct
import sys

def format_mac_address(bytes_addr):
    """Converts raw bytes into a human-readable MAC address (AA:BB:CC:DD:EE:FF)."""
    bytes_str = map("{:02x}".format, bytes_addr)
    return ":".join(bytes_str).upper()

def format_ip_address(bytes_addr):
    """Converts 4 bytes into a human-readable IPv4 address string."""
    return ".".join(map(str, bytes_addr))

def unpack_ethernet_frame(data):
    """Unpacks the 14-byte Ethernet header."""
    dest_mac, src_mac, proto = struct.unpack("! 6s 6s H", data[:14])
    return format_mac_address(dest_mac), format_mac_address(src_mac), socket.htons(proto), data[14:]

def unpack_ipv4_packet(data):
    """Unpacks the IPv4 header and extracts the payload protocol type."""
    version_and_header_length = data[0]
    # Extract the header length (lower 4 bits) and multiply by 4 to get bytes
    header_length = (version_and_header_length & 15) * 4
    
    # Unpack target fields: TTL, Protocol, Source IP, Destination IP
    # We slice up to 20 bytes (standard minimum IPv4 header size)
    _, _, _, _, ttl, proto, _, src, target = struct.unpack("! 8s B B H 4s 4s", data[:20])
    
    return ttl, proto, format_ip_address(src), format_ip_address(target), data[header_length:]

def start_sniffing():
    # Setup connection interface depending on OS platform
    if sys.platform == "win32":
        # Windows requires an IP-based socket connection loop
        conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        hostname = socket.gethostname()
        target_ip = socket.gethostbyname(hostname)
        conn.bind((target_ip, 0))
        # Include IP headers in captured packets
        conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        # Enable promiscuous mode to receive all fluid traffic
        conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    else:
        # Linux/macOS raw socket interface tracking all protocols at the link layer
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    print("=" * 60)
    print("[*] Raw Sniffer initialized. Monitoring incoming traffic lines...")
    print("=" * 60)

    try:
        while True:
            # Capture incoming buffer stream frames
            raw_data, addr = conn.recvfrom(65535)
            
            if sys.platform != "win32":
                # Step 1: Unpack Link Layer (Ethernet Frame)
                dest_mac, src_mac, eth_proto, ip_data = unpack_ethernet_frame(raw_data)
                
                # We only want to handle IPv4 traffic packets (Protocol 8 represents IPv4)
                if eth_proto == 8:
                    # Step 2: Unpack Network Layer (IPv4)
                    ttl, transport_proto, src_ip, dest_ip, payload = unpack_ipv4_packet(ip_data)
                    
                    print(f"\n[+] [ETHERNET FRAME]: {src_mac} -> {dest_mac}")
                    print(f"    |_ [IPv4 PACKET]: {src_ip} -> {dest_ip} | TTL: {ttl}")
                    
                    # Identify Common Transport Protocols
                    if transport_proto == 1:
                        print("       |_ [Protocol]: ICMP (Ping request/reply)")
                    elif transport_proto == 6:
                        print("       |_ [Protocol]: TCP (Web traffic, SSH, file transfers)")
                    elif transport_proto == 17:
                        print("       |_ [Protocol]: UDP (DNS, streaming media)")
            else:
                # Windows skips directly to the Network Layer via the RAW socket setup
                ttl, transport_proto, src_ip, dest_ip, payload = unpack_ipv4_packet(raw_data)
                print(f"\n[+] [IPv4 PACKET]: {src_ip} -> {dest_ip} | TTL: {ttl} | Protocol: {transport_proto}")

    except KeyboardInterrupt:
        print("\n[-] Sniffer deactivated. Closing connection buffers safely.")
        if sys.platform == "win32":
            conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit(0)

if __name__ == "__main__":
    start_sniffing()
