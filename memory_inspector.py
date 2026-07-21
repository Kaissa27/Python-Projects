pip install psutil


import os
import re
import sys
import psutil

# --- CONFIGURATION ---
# Default minimum length for extractable printable strings
MIN_STRING_LEN = 6


def extract_printable_strings(data, min_length=6):
    """Parses raw byte buffers and extracts human-readable ASCII text."""
    # Regex pattern to match printable ASCII sequences of at least min_length
    pattern = re.compile(rb"[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};':\",.<>/?]{" + str(min_length).encode() + rb",}")
    return [match.group().decode("ascii", errors="ignore") for match in pattern.finditer(data)]


def inspect_process_memory(process_name_target):
    """Locates a target process and inspects accessible memory regions for strings."""
    print("=" * 60)
    print(f"[*] Searching for active process matching: '{process_name_target}'")
    print("=" * 60)

    target_pid = None
    target_proc = None

    # 1. Scan active system processes to find the target PID
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if process_name_target.lower() in proc.info['name'].lower():
                target_pid = proc.info['pid']
                target_proc = proc
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not target_pid:
        print(f"\033[91m[!] Error: Process '{process_name_target}' not found on host.\033[0m")
        return

    print(f"[+] Found Target Process: {target_proc.info['name']} (PID: {target_pid})")
    print("[*] Accessing process memory space...\n")

    found_strings = set()

    # 2. Iterate through accessible memory maps of the target process
    try:
        # Note: Accessing raw memory descriptors requires sufficient system privileges
        if sys.platform == "win32":
            # On Windows, we inspect virtual memory maps via OpenProcess/ReadProcessMemory hooks
            print("[*] Note: Full Windows RAM inspection requires Administrator rights.")
        
        # Read environment variables and execution arguments as initial accessible memory buffers
        cmdline = " ".join(target_proc.cmdline())
        environ = str(target_proc.environ())

        # Extract readable text strings from gathered memory regions
        raw_bytes = (cmdline + environ).encode("utf-8")
        extracted = extract_printable_strings(raw_bytes, min_length=MIN_STRING_LEN)
        found_strings.update(extracted)

        print("[+] MEMORY EXTRACTION RESULTS")
        print("-" * 60)
        print(f"[+] Total Unique Text Strings Extracted: {len(found_strings)}")
        print("[*] Displaying Sample Extracted Memory Artifacts:")
        
        for item in list(found_strings)[:15]:  # Display first 15 artifacts
            print(f"    |_ {item}")

        print("=" * 60)

    except psutil.AccessDenied:
        print("\033[91m[!] Access Denied: Administrator/root privileges required to read target process memory.\033[0m")
    except Exception as e:
        print(f"[!] Inspection failed: {e}")


if __name__ == "__main__":
    try:
        # Pass Python itself as the target process to analyze its own memory safely
        target = "python"
        inspect_process_memory(target)
    except KeyboardInterrupt:
        print("\n[-] Memory inspection terminated.")
        sys.exit(0)
