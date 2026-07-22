import math
import os
import re
import sys

# --- SECRET REGEX PATTERNS ---
# Common regex patterns used to identify sensitive credential formats
SECRET_PATTERNS = {
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "Generic API Key / Secret": r"(?i)(api_key|secret_key|access_token|password|auth_token)\s*=\s*['\"]([A-Za-z0-9_\-\.]{16,})['\"]",
    "RSA / Private Key Header": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
    "JSON Web Token (JWT)": r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_#-]+",
    "Generic High Entropy String": r"['\"]([A-Za-z0-9+/=]{32,})['\"]"
}


def calculate_shannon_entropy(data):
    """Calculates Shannon Entropy to measure randomness in a string (useful for spotting cryptographic keys)."""
    if not data:
        return 0
    entropy = 0
    for x in set(data):
        p_x = float(data.count(x)) / len(data)
        entropy -= p_x * math.log2(p_x)
    return entropy


def scan_file_for_secrets(file_path):
    """Inspects a single file line-by-line for matched patterns and high-entropy strings."""
    findings = []
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, start=1):
                clean_line = line.strip()

                # 1. Match against known secret regex signatures
                for key_type, pattern in SECRET_PATTERNS.items():
                    matches = re.finditer(pattern, clean_line)
                    for match in matches:
                        matched_text = match.group(0)
                        findings.append({
                            "line": line_num,
                            "type": key_type,
                            "snippet": matched_text[:40] + ("..." if len(matched_text) > 40 else ""),
                            "entropy": round(calculate_shannon_entropy(matched_text), 2)
                        })

    except Exception as e:
        print(f"[!] Unable to read file {file_path}: {e}")

    return findings


def run_code_audit(target_directory):
    print("=" * 65)
    print("         STATIC CODE AUDITOR & SECRET DETECTOR ENGINE         ")
    print("=" * 65)
    print(f"[*] Starting recursion scan in directory: {target_directory}")
    print("[*] Auditing files for hardcoded keys, tokens, and credentials...\n")

    total_files = 0
    flagged_files = 0

    # Walk through directory recursively
    for root, _, files in os.walk(target_directory):
        for file in files:
            # Skip binary/image files and git metadata to keep scan focused
            if file.endswith((".py", ".json", ".env", ".yaml", ".yml", ".txt", ".js")):
                total_files += 1
                file_path = os.path.join(root, file)
                
                results = scan_file_for_secrets(file_path)
                
                if results:
                    flagged_files += 1
                    print(f"\033[91m[VULNERABILITY] Potential Secret Exposed in File: {file_path}\033[0m")
                    for item in results:
                        print(f"   |_ Line {item['line']:<4} | Type: {item['type']}")
                        print(f"      |_ Value:   {item['snippet']}")
                        print(f"      |_ Entropy: {item['entropy']} (High randomness threshold)")
                    print("-" * 65)

    print("\n" + "=" * 65)
    print("                   SECURITY AUDIT SUMMARY                     ")
    print("=" * 65)
    print(f"[+] Total Code Files Inspected: {total_files}")
    if flagged_files == 0:
        print("\033[92m[+] SUCCESS: No exposed secrets detected across audited files.\033[0m")
    else:
        print(f"\033[91m[!] WARNING: Found potential secrets in {flagged_files} file(s)!\033[0m")
    print("=" * 65)


if __name__ == "__main__":
    try:
        # Default scan directory set to current working path
        scan_directory = "."
        run_code_audit(scan_directory)
    except KeyboardInterrupt:
        print("\n[-] Secret scanner terminated by user.")
        sys.exit(0)
