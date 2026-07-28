import binascii
import hashlib
import secrets
import sys

# --- SIMULATED ACTIVE DIRECTORY DATABASE ---
# Domain Service Principal Names (SPNs) bound to specific domain accounts
MOCK_SPN_DIRECTORY = [
    {
        "spn": "MSSQLSvc/db-prod-01.corp.local:1433",
        "account_name": "svc_sql_admin",
        "domain": "CORP.LOCAL",
        "password_hash_ntlm": hashlib.new("md4", "Password123!".encode("utf-16le")).hexdigest(),
        "is_service_account": True
    },
    {
        "spn": "HTTP/web-portal.corp.local",
        "account_name": "svc_web",
        "domain": "CORP.LOCAL",
        "password_hash_ntlm": hashlib.new("md4", "ComplexP@ss2026!".encode("utf-16le")).hexdigest(),
        "is_service_account": True
    },
    {
        "spn": "HOST/DC01.corp.local",
        "account_name": "DC01$",
        "domain": "CORP.LOCAL",
        "password_hash_ntlm": secrets.token_hex(16),  # Machine accounts have complex 128-char random passwords
        "is_service_account": False
    }
]


def emulate_tgs_request(spn_entry):
    """Simulates a Domain Controller issuing an encrypted TGS Ticket for a requested SPN."""
    # Generate mock Ticket Granting Service (TGS) metadata
    ticket_flags = "40810000"
    cipher_type = "23"  # RC4-HMAC encryption type (ETYPE 23)
    
    # Generate a dummy encrypted ticket payload using random bytes as ciphertext
    mock_ticket_bytes = secrets.token_bytes(64)
    mock_checksum = secrets.token_bytes(16)

    # Format into standard Hashcat $krb5tgs$ structure (Mode 13100 - Kerberos 5 TGS-REP etype 23)
    # Format: $krb5tgs$etype$*user*domain*spn*$checksum$cipher
    user = spn_entry["account_name"]
    domain = spn_entry["domain"]
    spn = spn_entry["spn"]
    
    checksum_hex = binascii.hexlify(mock_checksum).decode("utf-8")
    cipher_hex = binascii.hexlify(mock_ticket_bytes).decode("utf-8")

    hashcat_formatted = (
        f"$krb5tgs${cipher_type}$*{user}*{domain}*{spn}*${checksum_hex}${cipher_hex}"
    )

    return hashcat_formatted


def run_kerberoast_audit():
    print("=" * 65)
    print("      ACTIVE DIRECTORY KERBEROASTING & SPN AUDIT SIMULATOR      ")
    print("=" * 65)
    print("[*] Enumerating Domain Service Principal Names (SPNs)...")
    print(f"[*] Found {len(MOCK_SPN_DIRECTORY)} total SPN record(s) registered in directory.\n")

    kerberoastable_targets = []

    # 1. SPN Discovery & Targeting
    for entry in MOCK_SPN_DIRECTORY:
        print(f"[*] Inspecting SPN: {entry['spn']}")
        print(f"    |_ Associated Account: {entry['account_name']}")
        
        # Filter out Computer/Machine accounts (ending in $) because their passwords are 128-char random strings
        if entry["account_name"].endswith("$"):
            print("    \033[90m|_ Skip: Machine account (non-crackable random password)\033[0m")
        else:
            print("\033[91m    [!] VULNERABLE: Service User Account targets identified!\033[0m")
            kerberoastable_targets.append(entry)

    print("\n" + "-" * 65)
    print(f"[*] Requesting TGS Service Tickets for {len(kerberoastable_targets)} target(s)...")
    print("-" * 65 + "\n")

    # 2. Simulate TGS Ticket Extraction & Hashcat Export
    extracted_hashes = []
    for target in kerberoastable_targets:
        hash_output = emulate_tgs_request(target)
        extracted_hashes.append((target["account_name"], hash_output))
        
        print(f"\033[92m[+] TGS REP Extracted for Service: {target['account_name']}\033[0m")
        print(f"   |_ Hashcat Format (Mode 13100):")
        print(f"      {hash_output[:75]}...")
        print()

    # 3. Save extracted hashes to offline wordlist file
    output_filename = "kerberoast_hashes.txt"
    with open(output_filename, "w") as f:
        for _, h in extracted_hashes:
            f.write(h + "\n")

    print("=" * 65)
    print("                    AUDIT SUMMARY REPORT                      ")
    print("=" * 65)
    print(f"[+] Total Service Accounts Kerberoasted : {len(extracted_hashes)}")
    print(f"[+] Formatted Hashes Exported To        : '{output_filename}'")
    print("[*] Recommended Remediation : Enforce Managed Service Accounts (gMSA) or >= 25-char passwords.")
    print("=" * 65)


if __name__ == "__main__":
    try:
        run_kerberoast_audit()
    except KeyboardInterrupt:
        print("\n[-] Kerberoasting simulation stopped.")
        sys.exit(0)
