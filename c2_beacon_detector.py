from collections import defaultdict
import datetime
import math
import re
import statistics
import sys

# --- CONFIGURATION ---
# Maximum standard deviation (in seconds) between connections to classify as a rigid beacon
JITTER_THRESHOLD_SECONDS = 1.5
MIN_CONNECTIONS_REQUIRED = 4

# Simulated firewall / NetFlow flow logs (Format: Timestamp, Source IP, Destination IP, Port)
MOCK_NETFLOW_LOGS = [
    "2026-07-26 10:00:00 | Src: 192.168.1.15 | Dst: 93.184.216.34:443",   # Regular Web Browsing
    "2026-07-26 10:00:05 | Src: 192.168.1.100 | Dst: 198.51.100.42:8080", # C2 Beacon 1
    "2026-07-26 10:00:12 | Src: 192.168.1.15 | Dst: 93.184.216.34:443",   # Irregular delay (7s)
    "2026-07-26 10:00:15 | Src: 192.168.1.100 | Dst: 198.51.100.42:8080", # C2 Beacon 2 (10s delta)
    "2026-07-26 10:00:25 | Src: 192.168.1.100 | Dst: 198.51.100.42:8080", # C2 Beacon 3 (10s delta)
    "2026-07-26 10:00:29 | Src: 192.168.1.15 | Dst: 93.184.216.34:443",   # Irregular delay (17s)
    "2026-07-26 10:00:35 | Src: 192.168.1.100 | Dst: 198.51.100.42:8080", # C2 Beacon 4 (10s delta)
    "2026-07-26 10:00:45 | Src: 192.168.1.100 | Dst: 198.51.100.42:8080", # C2 Beacon 5 (10s delta)
]


def parse_timestamp(ts_str):
    """Converts a standard log string timestamp into a Python datetime object."""
    return datetime.datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")


def analyze_beacon_patterns(log_entries):
    """Groups connection events by flow pair and calculates statistical variance between hits."""
    print("=" * 65)
    print("       C2 COMMAND & CONTROL BEACONING DETECTION ENGINE        ")
    print("=" * 65)
    print(f"[*] Analyzing {len(log_entries)} NetFlow log events...")
    print(f"[*] Max Allowed Standard Deviation Threshold: <= {JITTER_THRESHOLD_SECONDS}s\n")

    # Map flow key tuple (Src_IP, Dst_IP_Port) -> list of datetime timestamps
    flow_tracker = defaultdict(list)

    log_pattern = re.compile(
        r"^(?P<time>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+\|\s+Src:\s+(?P<src>[\d\.]+)\s+\|\s+Dst:\s+(?P<dst>[\d\.]+:\d+)"
    )

    # 1. Parse log records into structured flows
    for line in log_entries:
        match = log_pattern.match(line)
        if match:
            ts = parse_timestamp(match.group("time"))
            src = match.group("src")
            dst = match.group("dst")
            flow_tracker[(src, dst)].append(ts)

    # 2. Evaluate statistical metrics per network flow
    suspicious_beacons = 0

    for (src, dst), timestamps in flow_tracker.items():
        if len(timestamps) < MIN_CONNECTIONS_REQUIRED:
            continue

        # Sort timestamps chronologically to calculate deltas
        timestamps.sort()
        deltas = [(timestamps[i] - timestamps[i - 1]).total_seconds() for i in range(1, len(timestamps))]

        avg_interval = statistics.mean(deltas)
        # Standard deviation measures the consistency of the time intervals (jitter)
        std_dev = statistics.stdev(deltas) if len(deltas) > 1 else 0.0

        print(f"[*] Flow Pair: [{src}] -> [{dst}]")
        print(f"    |_ Connection Count: {len(timestamps)}")
        print(f"    |_ Avg Interval    : {avg_interval:.2f} seconds")
        print(f"    |_ Time Std Dev    : {std_dev:.2f} seconds")

        # Low standard deviation indicates rigid periodic timing (typical for automated beacons)
        if std_dev <= JITTER_THRESHOLD_SECONDS:
            suspicious_beacons += 1
            print(f"\033[91m    [!] CRITICAL ALERT: High-Confidence C2 Beacon Detected!")
            print(f"        |_ Pattern exhibits rigid time delta ({avg_interval:.1f}s +/- {std_dev:.2f}s jitter)\033[0m")
        else:
            print("    \033[92m|_ Assessment: Normal user/bursty traffic pattern\033[0m")

        print("-" * 65)

    print("\n" + "=" * 65)
    print("                    ANALYSIS SUMMARY REPORT                   ")
    print("=" * 65)
    if suspicious_beacons > 0:
        print(f"\033[91m[!] WARNING: Detected {suspicious_beacons} active beaconing channel(s)!\033[0m")
    else:
        print("\033[92m[+] CLEAN: No regular C2 beaconing signatures identified.\033[0m")
    print("=" * 65)


if __name__ == "__main__":
    try:
        analyze_beacon_patterns(MOCK_NETFLOW_LOGS)
    except KeyboardInterrupt:
        print("\n[-] Beacon detector terminated.")
        sys.exit(0)
