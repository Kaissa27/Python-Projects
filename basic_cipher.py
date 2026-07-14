pip install cryptography


import os
import sys
from cryptography.fernet import Fernet

# --- INITIALIZATION HELPER ---
def generate_and_save_key():
    """Generates a fresh cryptographic key and saves it locally."""
    # Fernet handles the heavy math to create a secure key automatically
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("[+] A new key has been created and saved as 'secret.key'. Keep it safe!")

def load_key():
    """Loads the locally saved cryptographic key."""
    if not os.path.exists("secret.key"):
        generate_and_save_key()
    
    with open("secret.key", "rb") as key_file:
        return key_file.read()

# --- CORE MECHANICS ---
def encrypt_file(filename):
    """Reads a file, encrypts its contents, and overwrites it."""
    key = load_key()
    cipher = Fernet(key)

    print(f"[*] Reading cleartext from: {filename}")
    try:
        with open(filename, "rb") as file:
            file_data = file.read()
        
        # Scramble the data using the key
        encrypted_data = cipher.encrypt(file_data)

        # Overwrite the original file with the secret scrambled text
        with open(filename, "wb") as file:
            file.write(encrypted_data)
        print(f"[+] File '{filename}' successfully encrypted!")
    except FileNotFoundError:
        print(f"[!] Error: The file '{filename}' does not exist.")

def decrypt_file(filename):
    """Reads an encrypted file, decrypts its contents, and restores the original text."""
    key = load_key()
    cipher = Fernet(key)

    print(f"[*] Reading encrypted data from: {filename}")
    try:
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        
        # Descramble the data using the key
        decrypted_data = cipher.decrypt(encrypted_data)

        # Restore the original cleartext back to the file
        with open(filename, "wb") as file:
            file.write(decrypted_data)
        print(f"[+] File '{filename}' successfully decrypted back to normal!")
    except Exception as e:
        print(f"[!] Decryption failed. Was the file tampered with or is the key wrong? Details: {e}")

# --- SETUP MOCK ENVIRONMENT ---
def create_sample_file():
    """Creates a temporary text file to test the script safely."""
    with open("top_secret.txt", "w") as f:
        f.write("CONFIDENTIAL DATA: The password to the server is Admin123! Do not share.")
    print("[*] Created a test file named 'top_secret.txt' with sample text.")

if __name__ == "__main__":
    create_sample_file()
    
    # 1. Encrypt the file
    print("\n--- Running Encryption Phase ---")
    encrypt_file("top_secret.txt")
    
    # Let's inspect what the file looks like right now
    with open("top_secret.txt", "r", errors="ignore") as f:
        print(f"[*] Current scrambled file contents look like: \n    {f.read()}")

    # 2. Decrypt the file back to its original form
    print("\n--- Running Decryption Phase ---")
    decrypt_file("top_secret.txt")
    
    with open("top_secret.txt", "r") as f:
        print(f"[*] Restored file contents: \n    {f.read()}")
