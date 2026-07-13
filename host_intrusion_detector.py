pip install psutil

import datetime
import os
import sys
import time
import psutil

# --- CONFIGURATION ---
# Behavioral indicators frequently mapped to post-exploitation reconnaissance
SUSPICIOUS_PROCESS_NAMES = {
    "whoami", "netstat", "nmap", "mimikatz", "vssadmin", "powershell.exe", 
    "cmd.exe", "nc", "netcat", "ncat", "socat"
}

# Directories that shouldn't see unexpected binary execution changes
CRITICAL_BIN_PATH_KEYWORDS = ["/bin", "/sbin", "/tmp", "system32", "syswow64"]

ALERT_LOG = "hids_security_events.log"


def log_alert(event_type, description, process_metadata):
    """Formats and writes a structured behavioral alert down to a secure log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_msg = f"[{timestamp}] HIDS ALERT: {event_type} - {description}\n"
    alert_msg += f"   |_ Process Name: {process_metadata.get('name')} | PID: {process_metadata.get('pid')}\n"
    alert_msg += f"   |_ Executable Path: {process_metadata.get('exe')}\n"
    alert_msg += f"   |_ Command Line: { ' '.join(process_metadata.get('cmdline', [])) }\n"
    alert_msg += f"   |_ Parent PID: {process_metadata.get('ppid')} | User Context: {process_metadata.get('username')}\n"
    
    # Print in high-visibility bold yellow text inside the administration console
    print(f"\033[93m{alert_msg}\033[0m")
    
    with open(ALERT_LOG, "a") as f:
        f.write(alert_msg + "="*60 + "\n")


def scan_running_processes(monitored_pids):
    """Queries active kernel tables to detect anomalous execution indicators."""
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'ppid', 'username']):
        try:
            pid = proc.info['pid']
            
            # Skip evaluation cycles if we have already analyzed this process loop instance
            if pid in monitored_pids:
                continue
                
            # Add new process tracking frame
            monitored_pids.add(pid)
            
            proc_name = proc.info['name'].lower() if proc.info['name'] else ""
            proc_exe = proc.info['exe'].lower() if proc.info['exe'] else ""
            cmdline_str = " ".join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ""

            # Check Indicator Profile 1: Is a known reconnaissance or dual-use tool executing?
            if any(susp_name in proc_name for susp_name in SUSPICIOUS_PROCESS_NAMES):
                log_alert(
                    "Suspicious Tool Invocation", 
                    "A process matching known post-exploitation or discovery tools was spawned.", 
                    proc.info
                )
                continue

            # Check Indicator Profile 2: Is execution originating from a highly volatile directory?
            # Attackers commonly drop or execute payloads directly out of /tmp or user space configurations
            if "/tmp" in proc_exe or "appdata\\local\\temp" in proc_exe:
                log_alert(
                    "Volatile Execution Space Violation", 
                    "Binary execution identified running straight out of a temporary directory structure.", 
                    proc.info
                )
                continue

            # Check Indicator Profile 3: Suspicious arguments passed in the command line matrix
            if "downloadstring" in cmdline_str or "wget" in cmdline_str or "curl" in cmdline_str:
                log_alert(
                    "Network Payload Fetch Detected", 
                    "Command line arguments contain explicit metadata signatures for active web downloads.", 
                    proc.info
                )
                continue

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Short-lived system processes that exited or dropped permissions mid-inspection phase
            continue


def main():
    print("=" * 60)
    print("     HOST-BASED INTRUSION DETECTION SYSTEM (HIDS) DAEMON     ")
    print("=" * 60)
    print(f"[*] Core engine initialized. Appending forensic alerts to: ./{ALERT_LOG}")
    print("[*] Monitoring host process trees for behavioral anomalies... Press Ctrl+C to stop.")
    
    # Cache existing PIDs to establish a startup baseline before entering the evaluation loop
    monitored_pids = {p.pid for p in psutil.process_iter()}
    
    try:
        while True:
            scan_running_processes(monitored_pids)
            
            # Prune out PIDs from our memory map that are no longer active on the host
            active_pids = {p.pid for p in psutil.process_iter()}
            monitored_pids = monitored_pids.intersection(active_pids)
            
            # Sleep for a fraction of a second to prevent CPU starvation cycles
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n[-] Deactivating security daemon loops cleanly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
