import hashlib
import os
import sys
import time

# --- CONFIGURATION ---
CANARY_DIR = "./canary_zone"
CANARY_FILES = {
    "financial_records_2026.docx": "CONFIDENTIAL_FINANCIAL_DATA_CANARY_STRING_A1B2C3D4",
    "passwords_backup.xlsx": "SECRET_KEY_CANARY_TRIPWIRE_DATA_88990011"
}
POLL_INTERVAL = 2.0  # Seconds between monitor sweeps


def calculate_hash(content_bytes):
    """Generates a SHA-256 hash string for raw byte data."""
    return hashlib.sha256(content_bytes).hexdigest()


def deploy_canaries(target_dir):
    """Deploys initial canary decoy files and records their baseline state."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    canary_baselines = {}

    for filename, content in CANARY_FILES.items():
        file_path = os.path.join(target_dir, filename)
        content_bytes = content.encode("utf-8")
        
        # Write decoy file to disk
        with open(file_path, "wb") as f:
            f.write(content_bytes)

        # Record initial baseline hash and size
        canary_baselines[file_path] = {
            "hash": calculate_hash(content_bytes),
            "size": len(content_bytes)
        }
        print(f"[+] Canary Deployed: {file_path}")

    return canary_baselines


def start_canary_monitor():
    print("=" * 60)
    print("      RANSOMWARE CANARY & TRIPWIRE DETECTION ENGINE      ")
    print("=" * 60)
    print(f"[*] Deploying decoy files into path: {os.path.abspath(CANARY_DIR)}")
    
    baselines = deploy_canaries(CANARY_DIR)
    
    print("\n[*] Canary files active and baseline verified.")
    print(f"[*] Activating real-time integrity sweeps (Frequency: Every {POLL_INTERVAL}s)...")
    print("[*] Press Ctrl+C to stop monitoring.\n")

    while True:
        for file_path, base_info in baselines.items():
            filename = os.path.basename(file_path)

            # 1. Check if the canary file was deleted or renamed (common ransomware behavior)
            if not os.path.exists(file_path):
                print(f"\n\033[91m[CRITICAL ALERT] CANARY FILE DELETED OR RENAMED!")
                print(f"   |_ Target Path: {file_path}")
                print("   |_ Security Action: Potential bulk file-encryption attack in progress!\033[0m")
                continue

            # 2. Check if the file contents or file size have been altered
            try:
                with open(file_path, "rb") as f:
                    current_data = f.read()
                    
                current_hash = calculate_hash(current_data)
                current_size = len(current_data)

                if current_hash != base_info["hash"]:
                    print(f"\n\033[91m[CRITICAL ALERT] RANSOMWARE ACTIVITY SUSPECTED!")
                    print(f"   |_ Canary File Modified: {filename}")
                    print(f"   |_ Expected SHA-256 : {base_info['hash'][:16]}...")
                    print(f"   |_ Current SHA-256  : {current_hash[:16]}...")
                    print(f"   |_ Expected Size    : {base_info['size']} bytes | Current Size: {current_size} bytes")
                    print("   |_ Threat Assessment: File corrupted or encrypted by unauthorized process!\033[0m")

            except Exception as e:
                print(f"[!] Access error on canary file {filename}: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        start_canary_monitor()
    except KeyboardInterrupt:
        print("\n[-] Canary monitor deactivated cleanly.")
        sys.exit(0)
