import csv
from collections import Counter
import re

# --- CONFIGURATION ---
# A regex pattern to parse standard Combined Log Format (common for Nginx/Apache)
# Example log: 192.168.1.100 - - [04/Jul/2026:12:34:56 +0000] "POST /login HTTP/1.1" 401 234
LOG_PATTERN = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?"(?P<method>\s*?GET|POST|PUT|DELETE)?\s+(?P<path>.*?)\s+HTTP/.*?"\s+(?P<status>\d{3})'


def generate_mock_log():
    """Generates a dummy log file for testing purposes."""
    mock_data = """192.168.1.45 - - [04/Jul/2026:23:01:00 +0000] "POST /login HTTP/1.1" 401 512
192.168.1.45 - - [04/Jul/2026:23:01:05 +0000] "POST /login HTTP/1.1" 401 512
192.168.1.45 - - [04/Jul/2026:23:01:10 +0000] "POST /login HTTP/1.1" 401 512
192.168.1.102 - - [04/Jul/2026:23:02:15 +0000] "GET /index.html HTTP/1.1" 200 4324
192.168.1.45 - - [04/Jul/2026:23:02:20 +0000] "POST /login HTTP/1.1" 200 1024
192.168.1.200 - - [04/Jul/2026:23:03:01 +0000] "GET /hidden-profile HTTP/1.1" 403 240
192.168.1.102 - - [04/Jul/2026:23:04:12 +0000] "GET /broken-link HTTP/1.1" 404 120
192.168.1.200 - - [04/Jul/2026:23:05:00 +0000] "GET /hidden-profile HTTP/1.1" 403 240
"""
    with open("server.log", "w") as f:
        f.write(mock_data)
    print("[+] Generated temporary 'server.log' file for testing.")


def analyze_logs(log_file_path):
    ip_counter = Counter()
    status_counter = Counter()
    failed_logins = Counter()

    compiled_regex = re.compile(LOG_PATTERN)

    print(f"[*] Parsing log file: {log_file_path}")

    # Process line-by-line (Memory efficient for large files)
    with open(log_file_path, "r") as file:
        for line in file:
            match = compiled_regex.match(line)
            if match:
                data = match.groupdict()
                ip = data["ip"]
                status = data["status"]
                path = data["path"]

                ip_counter[ip] += 1
                status_counter[status] += 1

                # Flag potential brute-force or malicious scanning
                if status == "401" and "/login" in path:
                    failed_logins[ip] += 1

    return ip_counter, status_counter, failed_logins


def export_report(ip_counts, status_counts, alert_ips, report_path):
    print(f"[*] Exporting security audit report to: {report_path}")

    with open(report_path, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Section 1: Traffic Breakdown
        writer.writerow(["--- IP TRAFFIC SUMMARY ---"])
        writer.writerow(["IP Address", "Request Count"])
        for ip, count in ip_counts.most_common():
            writer.writerow([ip, count])

        writer.writerow([])  # Blank spacer row

        # Section 2: HTTP Status Codes
        writer.writerow(["--- HTTP STATUS CODE SUMMARY ---"])
        writer.writerow(["Status Code", "Occurrences"])
        for status, count in status_counts.most_common():
            writer.writerow([status, count])

        writer.writerow([])

        # Section 3: Security Alerts
        writer.writerow(["--- SECURITY ALERTS (FAILED LOGINS >= 3) ---"])
        writer.writerow(["Suspect IP Address", "Failed Attempts"])
        for ip, count in alert_ips.items():
            if count >= 3:
                writer.writerow([ip, count])

    print("[+] Export complete.")


if __name__ == "__main__":
    # 1. Setup mock log data locally
    generate_mock_log()

    # 2. Run analysis mechanics
    ips, statuses, failures = analyze_logs("server.log")

    # 3. Print out a quick terminal overview
    print("\n=== AUDIT OVERVIEW ===")
    print(f"Top Attacking/Visiting IP: {ips.most_common(1)[0][0] if ips else 'None'}")
    print(f"Total 404 Errors Found: {statuses.get('404', 0)}")

    # 4. Save results structurally
    export_report(ips, statuses, failures, "audit_report.csv")
