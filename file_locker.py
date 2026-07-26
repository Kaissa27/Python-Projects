pip install cryptography

import os
import sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# --- CONFIGURATION ---
ITERATIONS = 100000  # PBKDF2 iteration count for key stretching
SALT_SIZE = 16       # 128-bit random salt
NONCE_SIZE = 12      # 96-bit standard AES-GCM nonce size


def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a 256-bit cryptographic key from a password using PBKDF2 with SHA-256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_file(file_path: str, password: str):
    """Encrypts a file using AES-256-GCM and embeds the salt and nonce in the output."""
    if not os.path.exists(file_path):
        print(f"\033[91m[!] Error: File '{file_path}' not found.\033[0m")
        return

    print(f"[*] Encrypting target file: {file_path}")

    # Generate cryptographically secure random salt and nonce
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    with open(file_path, "rb") as f:
        plaintext = f.read()

    # Encrypt the plaintext; AESGCM automatically appends a 128-bit authentication tag
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

    # Output structure: [SALT (16B)][NONCE (12B)][CIPHERTEXT + AUTH TAG]
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, "wb") as f:
        f.write(salt + nonce + ciphertext)

    print(f"\033[92m[+] SUCCESS: Encrypted file created -> {encrypted_file_path}\033[0m")


def decrypt_file(encrypted_file_path: str, password: str):
    """Decrypts an AES-256-GCM file and verifies authentication tag integrity."""
    if not os.path.exists(encrypted_file_path):
        print(f"\033[91m[!] Error: Encrypted file '{encrypted_file_path}' not found.\033[0m")
        return

    print(f"[*] Decrypting file: {encrypted_file_path}")

    with open(encrypted_file_path, "rb") as f:
        file_data = f.read()

    # Extract salt, nonce, and ciphertext payload
    if len(file_data) < SALT_SIZE + NONCE_SIZE:
        print("\033[91m[!] Error: Invalid or corrupted encrypted file structure.\033[0m")
        return

    salt = file_data[:SALT_SIZE]
    nonce = file_data[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = file_data[SALT_SIZE + NONCE_SIZE:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        # Decrypt and authenticate data in one step
        decrypted_data = aesgcm.decrypt(nonce, ciphertext, associated_data=None)

        # Restore original filename (stripping .enc extension if present)
        output_file_path = (
            encrypted_file_path[:-4] if encrypted_file_path.endswith(".enc") else encrypted_file_path + ".dec"
        )

        with open(output_file_path, "wb") as f:
            f.write(decrypted_data)

        print(f"\033[92m[+] SUCCESS: Decrypted file restored -> {output_file_path}\033[0m")

    except Exception:
        print("\033[91m[!] DECRYPTION FAILED: Incorrect password or tampered/corrupted file!\033[0m")


def run_demo():
    print("=" * 60)
    print("      AES-256 GCM AUTHENTICATED FILE ENCRYPTION ENGINE     ")
    print("=" * 60)

    demo_file = "confidential_notes.txt"
    demo_password = "SuperSecretMasterPassword123!"

    # 1. Create a dummy test file
    print(f"[*] Creating sample file: {demo_file}")
    with open(demo_file, "w") as f:
        f.write("CONFIDENTIAL DATA: System Access Keys & API Credentials - 2026\n")

    # 2. Encrypt the file
    print("\n--- ENCRYPTION STAGE ---")
    encrypt_file(demo_file, demo_password)

    # Clean up unencrypted original to complete locking step
    os.remove(demo_file)
    print(f"[*] Removed original unencrypted file: {demo_file}")

    # 3. Decrypt the file with correct password
    print("\n--- DECRYPTION STAGE (CORRECT PASSWORD) ---")
    decrypt_file(demo_file + ".enc", demo_password)

    # 4. Attempt decryption with wrong password to prove tag verification
    print("\n--- TAMPER / INVALID PASSWORD STAGE ---")
    decrypt_file(demo_file + ".enc", "WrongPassword456!")

    print("=" * 60)


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n[-] File locker operation canceled.")
        sys.exit(0)
