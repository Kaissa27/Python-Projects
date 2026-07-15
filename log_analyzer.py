import os
import re
import sys

# --- CONFIGURATION ---
LOG_FILE = "server_access.log"


def create_mock_log_file():
    """Generates a mock server log file containing both normal and suspicious events."""
    mock_logs = [
        "2026-07-15 10:00:01 - INFO - User admin logged in successfully from IP: 192.168.1.50\n",
        "2026-07-15 10:01:23 - WARNING - Failed login attempt for user guest from IP: 203.0.113.5\n",
        "2026-07-15 10:01:25 - WARNING - Failed login attempt for user guest from IP: 203.0.113.5\n",
        "2026-07-15 10:01:28 - WARNING - Failed login attempt for user guest from IP: 203.0.113.5\n",
        "2026-07-15 10:05:12 - INFO - User sarah logged in successfully from IP: 192.168.1.72\n",
        "2026-07-15 10:10:45 - CRITICAL - Unauthorized database access attempt detected from IP: 198.51.100.12\n",
        "2026-07-15 10:12:00 - INFO - Automated system backup completed successfully\n",
    ]
    
    with open(LOG_FILE, "w") as f:
        f.writelines(mock_logs)
    print(f"[+] Mock log file generated successfully: ./{LOG_FILE}")


def analyze_logs():
    """Reads the log file and flags lines containing security warnings or critical events."""
    if not os.path.exists(LOG_FILE):
        create_mock_log_file()

    print("\n" + "=" * 60)
    print(f"[*] Starting security analysis on log file: {LOG_FILE}")
    print("=" * 60)

    failed_login_count = 0
    critical_alerts = 0
    malicious_ips = set()

    # Simple Regular Expression to find IP addresses (4 sets of numbers separated by dots)
    ip_pattern = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")

    # Open and read the file line-by-line
    with open(LOG_FILE, "r") as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()

            # 1. Look for Failed Logins
            if "failed login" in line.lower():
                failed_login_count += 1
                # Find the IP address in this line using our regex pattern
                ip_match = ip_pattern.search(line)
                if ip_match:
                    malicious_ips.add(ip_match.group())
                print(f"[ALERT] Line {line_num}: Potential Brute-Force Attempt -> {line}")

            # 2. Look for Critical Anomalies
            elif "critical" in line.lower() or "unauthorized" in line.lower():
                critical_alerts += 1
                ip_match = ip_pattern.search(line)
                if ip_match:
                    malicious_ips.add(ip_match.group())
                print(f"\033[91m[CRITICAL] Line {line_num}: Severe Security Event -> {line}\033[0m")

    # Display Security Report
    print("\n" + "=" * 60)
    print("                    SECURITY AUDIT REPORT                   ")
    print("=" * 60)
    print(f"[+] Total Failed Login Attempts Detected: {failed_login_count}")
    print(f"[+] Critical Host Violations Flagged:    {critical_alerts}")
    print(f"[+] Unique Suspect IP Addresses Flagged: {', '.join(malicious_ips) if malicious_ips else 'None'}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        # Create the mock file first, then run the parser against it
        create_mock_log_file()
        analyze_logs()
    except KeyboardInterrupt:
        print("\n[-] Analysis aborted.")
        sys.exit(0)
