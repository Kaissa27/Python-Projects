import collections

def analyze_logs():
    # Simulated log data (as if read from a file 'server.log')
    # Format: [Timestamp] [Level] [IP Address] [Message] 
    raw_logs = [
        "[08:01] INFO 192.168.1.1 User Login",
        "[08:05] ERROR 192.168.1.50 Database Timeout",
        "[08:10] INFO 192.168.1.2 User Logout",
        "[08:12] ERROR 192.168.1.50 Connection Reset",
        "[08:15] WARN 172.16.0.5 Disk Space Low",
        "[08:20] ERROR 10.0.0.1 Critical Failure",
        "[08:22] INFO 192.168.1.1 Page Refresh"
    ]

    print("--- Log Analysis Automation ---")

    # 1. Parsing Phase: Extract the 'Level' and 'IP'
    # We split by space and take index 1 (Level) and 2 (IP)
    parsed_entries = []
    for line in raw_logs:
        parts = line.split(" ")
        level = parts[1]
        ip = parts[2]
        parsed_entries.append((level, ip))

    # 2. Filtering: Only get ERROR logs
    errors = [ip for level, ip in parsed_entries if level == "ERROR"]

    # 3. Frequency Analysis: Who is the "Top Offender"?
    # collections.Counter is a powerful tool for data scientists
    ip_counts = collections.Counter(errors)
    
    # 4. Reporting
    print(f"Total Logs Processed: {len(raw_logs)}")
    print(f"Errors Found:        {len(errors)}")
    
    print("\nError Distribution by IP:")
    for ip, count in ip_counts.items():
        print(f" - {ip}: {count} occurrences")

    # Identify the specific IP with the most errors
    if ip_counts:
        top_ip, top_count = ip_counts.most_common(1)[0]
        print(f"\n[!] ALERT: IP {top_ip} is the primary source of errors.")

if __name__ == "__main__":
    analyze_logs()
