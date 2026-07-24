import hashlib
import json
import os
import sys

# --- CONFIGURATION ---
TARGET_DIRECTORY = "./monitored_files"  # Directory path to monitor
BASELINE_FILE = "baseline.json"         # File storing verified hash states


def calculate_sha256(file_path):
    """Calculates the SHA-256 hash of a file reading in binary chunks."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read in 64KB chunks to efficiently hash large files
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"[!] Error reading file {file_path}: {e}")
        return None


def generate_baseline(directory):
    """Scans the target directory and creates a new baseline dictionary saved to JSON."""
    print("=" * 60)
    print(f"[*] GENERATING NEW FILE INTEGRITY BASELINE")
    print(f"[*] Target Directory: {os.path.abspath(directory)}")
    print("=" * 60 + "\n")

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"[+] Created target directory '{directory}'. Add test files here.")

    baseline = {}
    file_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_sha256(file_path)
            if file_hash:
                # Store relative file path to keep baseline portable
                rel_path = os.path.relpath(file_path, directory)
                baseline[rel_path] = file_hash
                file_count += 1
                print(f"[+] Baseline Hashed: {rel_path}")

    # Write baseline to local JSON storage
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print("\n" + "=" * 60)
    print(f"[SUCCESS] Recorded baseline for {file_count} file(s) -> saved to '{BASELINE_FILE}'.")
    print("=" * 60)


def verify_integrity(directory):
    """Compares the current file state in the directory against the stored baseline."""
    print("=" * 60)
    print(f"[*] AUDITING FILE INTEGRITY AGAINST BASELINE")
    print(f"[*] Target Directory: {os.path.abspath(directory)}")
    print("=" * 60 + "\n")

    if not os.path.exists(BASELINE_FILE):
        print(f"\033[91m[!] Baseline file '{BASELINE_FILE}' not found. Run baseline setup first.\033[0m")
        return

    with open(BASELINE_FILE, "r") as f:
        baseline = json.load(f)

    current_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, directory)
            file_hash = calculate_sha256(file_path)
            if file_hash:
                current_files[rel_path] = file_hash

    modifications_detected = False

    # 1. Check for modified or deleted files
    for rel_path, original_hash in baseline.items():
        if rel_path not in current_files:
            print(f"\033[91m[DELETED] File Missing: {rel_path}\033[0m")
            modifications_detected = True
        elif current_files[rel_path] != original_hash:
            print(f"\033[91m[MODIFIED] Hash Mismatch Detected: {rel_path}\033[0m")
            print(f"   |_ Baseline Hash: {original_hash[:16]}...")
            print(f"   |_ Current Hash:  {current_files[rel_path][:16]}...")
            modifications_detected = True

    # 2. Check for newly added untracked files
    for rel_path in current_files:
        if rel_path not in baseline:
            print(f"\033[93m[NEW FILE] Untracked File Created: {rel_path}\033[0m")
            modifications_detected = True

    print("\n" + "=" * 60)
    print("                    INTEGRITY AUDIT SUMMARY                   ")
    print("=" * 60)
    if not modifications_detected:
        print("\033[92m[+] INTEGRITY VERIFIED: All files match baseline signatures.\033[0m")
    else:
        print("\033[91m[!] INTEGRITY ALERT: Changes detected in monitored path!\033[0m")
    print("=" * 60)


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1].lower() == "--init":
            generate_baseline(TARGET_DIRECTORY)
        else:
            verify_integrity(TARGET_DIRECTORY)
    except KeyboardInterrupt:
        print("\n[-] Integrity check canceled.")
        sys.exit(0)
