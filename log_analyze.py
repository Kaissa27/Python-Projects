from collections import defaultdict
import datetime
import re
import sys

# --- CONFIGURATION ---
FAILED_ATTEMPT_THRESHOLD = 3

# Sample raw authentication logs (simulating /var/log/auth.log or event logs)
MOCK_LOG_DATA = [
    "Jul 22 10:01:05 server sshd[1024]: Failed password for root from 192.168.1.105 port 52110 ssh2",
    "Jul 22 10:01:12 server sshd[1024]: Failed password for root from 192.168.1.105 port 52112 ssh2",
    "Jul 22 10:01:18 server sshd[1024]: Failed password for invalid user admin from 192.168.1.105 port 52114 ssh2",
    "Jul 22 10:01:25 server sshd[1024]: Accepted password for user1 from 192.168.1.50 port 49820 ssh2",
    "Jul 22 10:02:01 server sshd[1025]: Failed password for user2 from 10.0.0.42 port 33100 ssh2",
    "Jul 22 10:02:40 server sshd[1024]: Failed password for root from 192.168.1.105 port 52120 ssh2",
    "Jul 22 10:03:10 server sshd[1026]: Accepted password for root from 192.168.1.100 port 61200 ssh2"
]


def parse_auth_logs(log_lines):
    """Parses log lines, extracts IP addresses and login statuses, and aggregates failed attempts."""
    print("=" * 60)
    print("          BASIC SECURITY INCIDENT LOG ANALYZER          ")
    print("=" * 60)
    print(f"[*] Processing {len(log_lines)} log entries...")
    print(f"[*] Alert Threshold: > {FAILED_ATTEMPT_THRESHOLD} failed attempts per IP\n")

    # Regular expression to extract timestamp, status, username, and source IP
    log_pattern = re.compile(
        r"^(?P<timestamp>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*?(?P<status>Failed|Accepted)\s+password\s+for\s+(?:invalid\s+user\s+)?(?P<user>\w+)\s+from\s+(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    )

    failed_attempts_by_ip = defaultdict(list)
    successful_logins = []

    for line in log_lines:
        match = log_pattern.search(line)
        if match:
            timestamp = match.group("timestamp")
            status = match.group("status")
            user = match.group("user")
            ip = match.group("ip")

            if status == "Failed":
                failed_attempts_by_ip[ip].append({"time": timestamp, "user": user})
            elif status == "Accepted":
                successful_logins.append({"time": timestamp, "user": user, "ip": ip})

    # 1. Display Successful Logins
    print("[+] SUCCESSFUL AUTHENTICATION EVENTS")
    print("-" * 60)
    for entry in successful_logins:
        print(f"    |_ [{entry['time']}] User: '{entry['user']}' from IP: {entry['ip']}")

    # 2. Evaluate Failed Logins Against Threat Thresholds
    print("\n[+] FAILED AUTHENTICATION & BRUTE-FORCE AUDIT")
    print("-" * 60)

    for ip, attempts in failed_attempts_by_ip.items():
        count = len(attempts)
        if count >= FAILED_ATTEMPT_THRESHOLD:
            print(f"\033[91m[ALERT] SUSPECTED BRUTE-FORCE ATTACK FROM: {ip}")
            print(f"   |_ Total Failed Attempts: {count}")
            print("   |_ Targeted Usernames: " + ", ".join(set(a['user'] for a in attempts)))
            print("   |_ Event Timestamps:")
            for a in attempts:
                print(f"      - [{a['time']}] Target User: {a['user']}")
            print("\033[0m")
        else:
            print(f"[*] IP {ip}: {count} failed attempt(s) (Below threat threshold)")

    print("=" * 60)


if __name__ == "__main__":
    try:
        parse_auth_logs(MOCK_LOG_DATA)
    except KeyboardInterrupt:
        print("\n[-] Log analysis stopped by user.")
        sys.exit(0)
