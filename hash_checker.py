import hashlib
import os
import sys

# --- CORE MECHANICS ---

def calculate_file_hash(filename):
    """Computes the SHA-256 hash fingerprint of a local file."""
    # Initialize the SHA-256 hashing engine
    sha256_engine = hashlib.sha256()

    try:
        # Open the file in 'rb' mode (Read Binary) to process raw file bytes
        with open(filename, "rb") as file:
            # Read the file in small 4096-byte blocks so we don't crash on huge files
            while chunk := file.read(4096):
                sha256_engine.update(chunk)
        
        # Return the final hexadecimal string representation of the hash
        return sha256_engine.hexdigest()
    
    except FileNotFoundError:
        print(f"[!] Error: The file '{filename}' could not be found.")
        return None


def monitor_file_integrity():
    print("=" * 50)
    print("        BASIC FILE INTEGRITY SNAPSHOT TOOL        ")
    print("=" * 50)

    # 1. Setup a dummy sample file for testing
    test_file = "system_config.txt"
    with open(test_file, "w") as f:
        f.write("SERVER_PORT=8080\nALLOW_ANONYMOUS=False\n")
    print(f"[+] Created sample test file: {test_file}")

    # 2. Capture the initial trusted baseline fingerprint
    print(f"[*] Calculating initial trusted baseline hash...")
    baseline_hash = calculate_file_hash(test_file)
    print(f"    |_ Trusted Hash: {baseline_hash}\n")

    input("Press Enter to simulate a system modification to the file... ")

    # 3. Simulate an unauthorized modification (like an attacker tampering with settings)
    with open(test_file, "a") as f:
        f.write("ALLOW_ANONYMOUS=True\n")  # Tampering attempt
    print(f"\n[!] Notice: '{test_file}' has been modified.")

    # 4. Re-calculate the hash and run the integrity audit
    print(f"[*] Re-calculating hash for validation check...")
    current_hash = calculate_file_hash(test_file)
    print(f"    |_ Current Hash: {current_hash}\n")

    # 5. Evaluate results
    print("=" * 50)
    print("               AUDIT MONITOR RESULT               ")
    print("=" * 50)
    if baseline_hash == current_hash:
        print("\033[92m[SUCCESS] Integrity verified! The file is safe and unaltered.\033[0m")
    else:
        print("\033[91m[ALERT] INTEGRITY VIOLATION DETECTED!")
        print("   |_ The file fingerprints do not match. Unauthorized modification has occurred!\033[0m")
    print("=" * 50)

    # Clean up the test file
    if os.path.exists(test_file):
        os.remove(test_file)


if __name__ == "__main__":
    try:
        monitor_file_integrity()
    except KeyboardInterrupt:
        print("\n[-] Exiting integrity checker.")
        sys.exit(0)
