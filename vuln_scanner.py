import re
import sys

# --- VULNERABILITY DATABASE SIMULATION ---
# A structured mapping of software name keywords to their known vulnerable versions and CVE codes
VULNERABILITY_DB = {
    "openssh": [
        {"vuln_version_pattern": r"7\.[0-8]", "cve": "CVE-2018-15473", "severity": "MEDIUM", "desc": "Username Enumeration vulnerability"},
        {"vuln_version_pattern": r"8\.5", "cve": "CVE-2021-41617", "severity": "HIGH", "desc": "Privilege escalation through authorized keys configuration"}
    ],
    "apache": [
        {"vuln_version_pattern": r"2\.4\.(49|50)", "cve": "CVE-2021-41773", "severity": "CRITICAL", "desc": "Path Traversal and Remote Code Execution"}
    ],
    "vsftpd": [
        {"vuln_version_pattern": r"2\.3\.4", "cve": "CVE-2011-2523", "severity": "CRITICAL", "desc": "Backdoor Command Execution via malicious :) smiley string"}
    ]
}


def parse_and_scan_banner(raw_banner):
    """Inspects a service banner against the signature matrix database."""
    print("\n" + "=" * 60)
    print(f"[*] Auditing Service Banner: '{raw_banner.strip()}'")
    print("=" * 60)
    
    # Normalize banner text to lowercase for seamless signature parsing
    normalized_banner = raw_banner.lower()
    vuln_found = False

    # 1. Identify which software product the banner matches
    for software_name, cve_rules in VULNERABILITY_DB.items():
        if software_name in normalized_banner:
            print(f"[+] Component Match Identified: Detected active instance of [{software_name.upper()}]")
            
            # 2. Extract out version numbers using basic regular expressions
            # This looks for numbers separated by dots (like 2.4.49 or 7.4)
            version_match = re.search(r"\d+\.\d+(\.\d+)?", raw_banner)
            if version_match:
                detected_version = version_match.group()
                print(f"[*] Extracted Product Version String: {detected_version}")
                
                # 3. Evaluate the extracted version against known CVE signature patterns
                for rule in cve_rules:
                    if re.search(rule["vuln_version_pattern"], detected_version):
                        vuln_found = True
                        print(f"\n\033[91m[VULNERABILITY ALERT] !! DETECTED KNOWN EXPLOIT VECTOR !!")
                        print(f"   |_ CVE Reference: {rule['cve']}")
                        print(f"   |_ Severity Level: [{rule['severity']}]")
                        print(f"   |_ Exploit Profile: {rule['desc']}\033[0m")
            else:
                print("[-] Software identified, but version string could not be verified.")

    if not vuln_found:
        print("\033[92m[+] Audit Clean: No signature rules matched this product configuration.\033[0m")
    print("=" * 60)


def run_vulnerability_assessment_simulation():
    print("=" * 60)
    print("        BASIC EMBEDDED VULNERABILITY ASSESSMENT ENGINE        ")
    print("=" * 60)

    # Mocking real service banners collected from a network banner grabber tool
    sample_collected_banners = [
        "SSH-2.0-OpenSSH_7.4p1 Debian-10+deb9u7",
        "Apache/2.4.49 (Unix) OpenSSL/1.1.1d",
        "220 vsFTPd 2.3.4",
        "SSH-2.0-OpenSSH_9.2p1 Ubuntu-2ubuntu1.3" # Modern safe version
    ]

    for banner in sample_collected_banners:
        parse_and_scan_banner(banner)


if __name__ == "__main__":
    try:
        run_vulnerability_assessment_simulation()
    except KeyboardInterrupt:
        print("\n[-] Assessment terminated.")
        sys.exit(0)
