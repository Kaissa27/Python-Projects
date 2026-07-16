import os
import platform
import subprocess
import sys

# --- CONFIGURATION ---
# We will scan a local IP space (change this to match your authorized test subnet)
SUBNET_PREFIX = "192.168.1."
START_IP = 1
END_IP = 10  # Keeping the range small for a quick basic test


def ping_host(ip_address):
    """Sends a single ping packet to an IP address to check if it is active."""
    # Determine the current operating system to adjust ping flags
    current_os = platform.system().lower()
    
    if current_os == "windows":
        # -n 1: Send exactly 1 packet
        # -w 1000: Wait 1000 milliseconds (1 second) for a response
        command = ["ping", "-n", "1", "-w", "1000", ip_address]
    else:
        # -c 1: Send exactly 1 packet
        # -W 1: Wait 1 second for a response
        command = ["ping", "-c", "1", "-W", "1", ip_address]

    # Run the command in the background without letting text flood the terminal screen
    try:
        # subprocess.run returns an object containing the exit code status
        result = subprocess.run(
            command, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
        # In standard networking tools, an exit code of 0 means a successful reply
        return result.returncode == 0
    except Exception:
        return False


def run_ping_sweep():
    print("=" * 50)
    print(f"[*] Starting Ping Sweep on Subnet: {SUBNET_PREFIX}{START_IP} to {END_IP}")
    print("=" * 50)

    active_hosts = []

    # Loop sequentially through the assigned host range
    for host_id in range(START_IP, END_IP + 1):
        target_ip = f"{SUBNET_PREFIX}{host_id}"
        print(f"[*] Pinging {target_ip}...", end="", flush=True)

        if ping_host(target_ip):
            print("\r[+] HOST IS ALIVE: " + target_ip)
            active_hosts.append(target_ip)
        else:
            print("\r[-] Host dead/silent: " + target_ip)

    # Output Summary Dashboard
    print("\n" + "=" * 50)
    print("                SCANNING SUMMARY                ")
    print("=" * 50)
    print(f"[+] Total Active Hosts Found: {len(active_hosts)}")
    if active_hosts:
        print("[*] Active IP List:")
        for ip in active_hosts:
            print(f"    |_ {ip}")
    print("=" * 50)


if __name__ == "__main__":
    try:
        run_ping_sweep()
    except KeyboardInterrupt:
        print("\n[!] Scan sequence halted by user control.")
        sys.exit(0)
