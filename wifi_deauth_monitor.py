pip install scapy

import sys
import time
from scapy.all import Dot11Deauth, Dot11Disas, RadioTap, sniff

# --- CONFIGURATION ---
# Threshold for alerts: how many deauth frames within a short window trigger an alarm
ALERT_THRESHOLD = 5

# Simple memory structure to track frame occurrences
frame_counter = {"deauth_count": 0, "last_alert_time": 0}


def process_packet(packet):
    """Inspects captured wireless frames for explicit deauthentication subtypes."""
    
    # Check if the packet contains an 802.11 Layer and specifically a Deauth or Disas frame
    if packet.haslayer(Dot11Deauth) or packet.haslayer(Dot11Disas):
        frame_counter["deauth_count"] += 1
        
        # Extract MAC addresses involved if present
        # addr1 = Destination, addr2 = Source (AP or Client), addr3 = BSSID (Router ID)
        src_mac = packet.addr2 if packet.addr2 else "UNKNOWN"
        dst_mac = packet.addr1 if packet.addr1 else "UNKNOWN"
        
        current_time = time.time()
        
        # Evaluate if the frequency of dropped frames indicates an active attack vector
        if frame_counter["deauth_count"] >= ALERT_THRESHOLD:
            # Prevent log flooding by limiting alerts to once every 5 seconds
            if current_time - frame_counter["last_alert_time"] > 5:
                print(f"\n\033[91m[ALERT] Wi-Fi Deauthentication Storm Detected!")
                print(f"   |_ Total Frames Logged: {frame_counter['deauth_count']}")
                print(f"   |_ Apparent Target Client: {dst_mac}")
                print(f"   |_ Spoofed/Originating AP: {src_mac}\033[0m")
                
                frame_counter["last_alert_time"] = current_time
                # Reset count after alerting to track the next burst window
                frame_counter["deauth_count"] = 0


def run_wifi_monitor():
    print("=" * 60)
    print("        BASIC 802.11 WIRELESS DEAUTHENTICATION MONITOR        ")
    print("=" * 60)
    print("[*] Initializing wireless frame audit interface...")
    print("[*] Scanning passive frame loops... Press Ctrl+C to stop.")
    print("=" * 60 + "\n")

    try:
        # Note: In a real-world scenario, your wireless interface must be set to 
        # 'Monitor Mode' (e.g., via airmon-ng) for scapy to capture management frames.
        # We use a broad sniff loop here; if no monitor interface is passed, it scans local traffic.
        sniff(prn=process_packet, store=0)

    except PermissionError:
        print("\n\033[91m[!] CRITICAL ERROR: Insufficient system privileges.")
        print("    |_ Capturing raw link-layer frames requires root/administrator access.\033[0m\n")
    except Exception as e:
        print(f"[!] Monitoring engine exception: {e}")


if __name__ == "__main__":
    try:
        run_wifi_monitor()
    except KeyboardInterrupt:
        print("\n[-] Wireless auditor daemon deactivated cleanly.")
        sys.exit(0)
