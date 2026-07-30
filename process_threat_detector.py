pip install psutil

import os
import sys
import psutil

# --- DEFENSIVE POLICY BASELINES ---
# Directories where legitimate system binaries rarely execute
SUSPICIOUS_EXEC_PATHS = [
    "/tmp",
    "/var/tmp",
    "/dev/shm",
    "\\appdata\\local\\temp",
    "\\users\\public"
]

# Standard core OS processes and their expected executable names
SYSTEM_CRITICAL_PROCESSES = ["lsass.exe", "svchost.exe", "sshd", "init"]


def inspect_system_processes():
    print("=" * 70)
    print("      ENDPOINT THREAT DETECTOR & PROCESS MEMORY INSPECTOR     ")
    print("=" * 70)
    print("[*] Enumerating active system processes and execution paths...\n")

    suspicious_count = 0
    total_inspected = 0

    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'ppid', 'username']):
        try:
            total_inspected += 1
            info = proc.info
            pid = info['pid']
            name = info['name'] or "Unknown"
            exe_path = info['exe'] or ""
            cmdline = info['cmdline'] or []
            ppid = info['ppid']
            user = info['username'] or "N/A"

            threat_flags = []

            # Rule 1: Flag processes running out of temporary/untrusted directories
            if exe_path:
                normalized_path = exe_path.lower()
                for sus_path in SUSPICIOUS_EXEC_PATHS:
                    if sus_path in normalized_path:
                        threat_flags.append(f"Executable running from untrusted path: '{exe_path}'")

            # Rule 2: Flag hidden processes (processes with missing or empty executable paths)
            if not exe_path and name not in ["System", "Idle", "kthreadd"]:
                threat_flags.append("Missing or obscured binary executable path on disk")

            # Rule 3: Detect potential masquerading (e.g., svchost running outside system directories)
            if name.lower() in ["svchost.exe", "lsass.exe"] and "system32" not in exe_path.lower():
                threat_flags.append(f"Process name masquerading! Critical binary running outside System32: '{exe_path}'")

            # If anomalies detected, display threat alert
            if threat_flags:
                suspicious_count += 1
                print(f"\033[91m[CRITICAL ALERT] Suspicious Process Detected! (PID: {pid})\033[0m")
                print(f"   |_ Process Name : {name}")
                print(f"   |_ Parent PID   : {ppid}")
                print(f"   |_ Executed By  : {user}")
                print(f"   |_ Command Line : {' '.join(cmdline[:5])}")
                for flag in threat_flags:
                    print(f"   \033[93m|_ Threat Flag  : {flag}\033[0m")
                print("-" * 70)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Ignore transient system processes or restricted permission handles
            continue

    print("\n" + "=" * 70)
    print("                    INSPECTION SUMMARY REPORT                 ")
    print("=" * 70)
    print(f"[+] Total Processes Inspected : {total_inspected}")
    if suspicious_count > 0:
        print(f"\033[91m[!] WARNING: Flagged {suspicious_count} process anomaly(ies) on host!\033[0m")
    else:
        print("\033[92m[+] CLEAN: No suspicious process behaviors detected.\033[0m")
    print("=" * 70)


if __name__ == "__main__":
    try:
        inspect_system_processes()
    except KeyboardInterrupt:
        print("\n[-] Endpoint process audit halted.")
        sys.exit(0)
