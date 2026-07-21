import platform
import re
import subprocess
import sys
import time

# --- CONFIGURATION ---
CHECK_INTERVAL_SECONDS = 5


def get_arp_table():
    """Fetches and parses the operating system's local ARP cache table."""
    current_os = platform.system().lower()
    
    # Run system command to print the ARP table
    try:
        if current_os == "windows":
            output = subprocess.check_output(["arp", "-a"]).decode("utf-8", errors="ignore")
        else:
            output = subprocess.check_output(["arp", "-n"]).decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[!] Error fetching ARP table: {e}")
        return {}

    # Extract IP and MAC address pairs using Regular Expressions
    # Matches patterns like 192.168.1.1 and 00-1A-2B-3C-4D-5E (or 00:1a:2b:3c:4d:5e)
    ip_mac_pattern = re.compile(
        r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+([0-9a-fa-f]{2}[:-][0-9a-fa-f]{2}[:-][0-9a-fa-f]{2}[:-][0-9a-fa-f]{2}[:-][0-9a-fa-f]{2}[:-][0-9a-fa-f]{2})"
    )

    arp_mappings = {}
    for match in ip_mac_pattern.finditer(output):
        ip, mac = match.groups()
        # Normalize MAC address formatting to lowercase with colons
        normalized_mac = mac.lower().replace("-", ":")
        arp_mappings[ip] = normalized_mac

    return arp_mappings


def inspect_arp_cache():
    """Analyzes the ARP mappings to detect duplicate MAC addresses."""
    arp_table = get_arp_table()
    
    if not arp_table:
        print("[-] ARP table is currently empty or inaccessible.")
        return

    # Invert the mapping: group IP addresses by their MAC address
    mac_to_ips = {}
    for ip, mac in arp_table.items():
        if mac not in mac_to_ips:
            mac_to_ips[mac] = []
        mac_to_ips[mac].append(ip)

    spoof_detected = False

    # Evaluate if any single MAC address is claiming multiple IP addresses
    for mac, ips in mac_to_ips.items():
        # Ignore broadcast MAC addresses (ff:ff:ff:ff:ff:ff)
        if mac == "ff:ff:ff:ff:ff:ff":
            continue

        if len(ips) > 1:
            spoof_detected = True
            print("\n\033[91m[ALERT] POSSIBLE ARP SPOOFING / POISONING DETECTED!")
            print(f"   |_ Conflict MAC Address: {mac}")
            print(f"   |_ Assigned to IPs:      {', '.join(ips)}")
            print("   |_ Security Risk: A single host is impersonating multiple network devices.\033[0m")

    if not spoof_detected:
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [OK] ARP Cache Clean ({len(arp_table)} entries verified).")


def run_monitor():
    print("=" * 60)
    print("         LOCAL ARP TABLE INTEGRITY MONITOR          ")
    print("=" * 60)
    print(f"[*] Starting periodic cache inspection every {CHECK_INTERVAL_SECONDS} seconds...")
    print("[*] Press Ctrl+C to deactivate monitoring loop.\n")

    while True:
        inspect_arp_cache()
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        run_monitor()
    except KeyboardInterrupt:
        print("\n[-] ARP integrity monitor deactivated cleanly.")
        sys.exit(0)
