import math
import re
import sys

def calculate_entropy(password):
    """Calculates the Shannon entropy (in bits) of a password."""
    if not password:
        return 0

    # Determine the character pool size (L) based on character types present
    pool_size = 0
    if re.search(r"[a-z]", password):
        pool_size += 26  # Lowercase letters
    if re.search(r"[A-Z]", password):
        pool_size += 26  # Uppercase letters
    if re.search(r"\d", password):
        pool_size += 10  # Digits
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        pool_size += 32  # Standard special characters (approximate)

    # If the password has unrecognized characters, default pool to 95 (all printable ASCII)
    if pool_size == 0:
        pool_size = 95

    # Entropy formula: H = L * log2(R)
    # L = Password Length, R = Pool Size
    entropy_bits = len(password) * math.log2(pool_size)
    return round(entropy_bits, 2)


def check_password_strength(password):
    """Evaluates a password against common security complexity checks."""
    checks = {
        "Length (min 12 chars)": len(password) >= 12,
        "Contains Uppercase [A-Z]": bool(re.search(r"[A-Z]", password)),
        "Contains Lowercase [a-z]": bool(re.search(r"[a-z]", password)),
        "Contains Digit [0-9]": bool(re.search(r"\d", password)),
        "Contains Special Character": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    }

    print("\n" + "=" * 50)
    print(f"[*] Analyzing Password: {password}")
    print("=" * 50)

    # 1. Print Checklist Results
    passed_checks = 0
    for requirement, passed in checks.items():
        status = "[+]" if passed else "[-]"
        print(f"{status} {requirement}")
        if passed:
            passed_checks += 1

    # 2. Calculate and Display Cryptographic Entropy
    entropy = calculate_entropy(password)
    print(f"\n[*] Cryptographic Entropy: {entropy} bits")

    # 3. Rate the Password
    if passed_checks == 5 and entropy >= 60:
        print("\033[92m[RATING] STRONG PASSWORD: Excellent defense against brute-forcing.\033[0m")
    elif passed_checks >= 3 and entropy >= 40:
        print("\033[93m[RATING] MODERATE PASSWORD: Consider adding length or special characters.\033[0m")
    else:
        print("\033[91m[RATING] WEAK PASSWORD: Highly vulnerable to dictionary attacks.\033[0m")
    print("=" * 50)


def main():
    print("=" * 50)
    print("        PASSWORD STRENGTH & ENTROPY CHECKER       ")
    print("=" * 50)
    
    # Prompt user for input
    user_password = input("Enter a password to test: ").strip()
    
    if not user_password:
        print("[!] Password field cannot be blank.")
        return

    check_password_strength(user_password)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Exiting checker.")
        sys.exit(0)
