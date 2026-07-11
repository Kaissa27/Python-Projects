pip install cryptography


import base64
import hashlib
import json
import os
import sys
import time
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes

# --- GLOBAL CONFIGURATION ---
USER_DATABASE = {}  # In-memory user table simulation


def generate_gateway_keys():
    """Generates an asymmetric RSA key pair for signing and verifying tokens."""
    print("[*] Initializing gateway cryptographic signing identity keys...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


PRIVATE_SIGNING_KEY, PUBLIC_VERIFICATION_KEY = generate_gateway_keys()


# --- HELPER UTILITIES ---
def base64url_encode(data: bytes) -> str:
    """Encodes bytes into a URL-safe Base64 string without trailing padding '=' signs."""
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def base64url_decode(data: str) -> bytes:
    """Decodes a URL-safe Base64 string back to bytes, re-appending necessary padding."""
    rem = len(data) % 4
    if rem > 0:
        data += "=" * (4 - rem)
    return base64.urlsafe_b64decode(data.encode("utf-8"))


# --- MANUAL JWT INTERFACES ---
def create_jwt(username, role, expiration_seconds=60) -> str:
    """Constructs a signed JSON Web Token manually from individual blocks."""
    # Step 1: Define the Header
    header = {"alg": "RS256", "typ": "JWT"}
    
    # Step 2: Define the Payload (Claims)
    payload = {
        "sub": username,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + expiration_seconds,
    }

    # Encode JSON structures to Base64Url strings
    encoded_header = base64url_encode(json.dumps(header).encode("utf-8"))
    encoded_payload = base64url_encode(json.dumps(payload).encode("utf-8"))

    # Step 3: Assemble Signing Input String
    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")

    # Step 4: Cryptographically sign the input using our Private RSA Key
    raw_signature = PRIVATE_SIGNING_KEY.sign(
        signing_input,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    encoded_signature = base64url_encode(raw_signature)

    # Return completed token package: header.payload.signature
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def verify_jwt(token: str) -> dict:
    """Verifies a JWT's structure, cryptographic signature, and expiration validity."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Malformed token structure.")

        encoded_header, encoded_payload, encoded_signature = parts
        signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
        signature = base64url_decode(encoded_signature)

        # 1. Cryptographically verify signature using the Gateway Public Key
        PUBLIC_VERIFICATION_KEY.verify(
            signature,
            signing_input,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        # 2. Decode claims payload data
        payload = json.loads(base64url_decode(encoded_payload).decode("utf-8"))

        # 3. Evaluate Temporal Claims (Check if token is expired)
        if time.time() > payload.get("exp", 0):
            print("[!] Token Verification Denied: Token has expired.")
            return None

        return payload

    except Exception as e:
        print(f"[!] Token Verification Denied: Cryptographic invalidation or structural failure. ({e})")
        return None


# --- APPLICATION BUSINESS LOGIC ---
def register_user(username, password, role="user"):
    """Salts and hashes credentials before committing to memory."""
    salt = os.urandom(16)
    # Perform standard SHA-256 password hashing stretching
    hasher = hashlib.sha256()
    hasher.update(salt + password.encode("utf-8"))
    password_hash = hasher.hexdigest()
    
    USER_DATABASE[username] = {"salt": salt, "hash": password_hash, "role": role}
    print(f"[+] User '{username}' successfully registered with role authorization: [{role}]")


def authenticate_user(username, password) -> str:
    """Validates parameters and issues a signed access token if correct."""
    if username not in USER_DATABASE:
        print("[!] Authentication Failure: User unrecognized.")
        return None

    user_record = USER_DATABASE[username]
    hasher = hashlib.sha256()
    hasher.update(user_record["salt"] + password.encode("utf-8"))
    
    if hasher.hexdigest() == user_record["hash"]:
        print(f"[+] Authentication successful for user: {username}")
        # Generate token
        return create_jwt(username, user_record["role"])
    
    print("[!] Authentication Failure: Incorrect credential matches.")
    return None


# --- RUN PROGRAM SIMULATION ---
if __name__ == "__main__":
    print("=" * 60)
    print("     JWT AUTHENTICATION SERVER & GATEWAY SIMULATOR     ")
    print("=" * 60)

    # 1. Register application sandbox accounts
    register_user("bob_developer", "DevPass123!", role="admin")
    register_user("alice_guest", "Welcome2026!", role="guest")

    print("\n[*] --- STEP 1: Simulating User Authentication ---")
    active_token = authenticate_user("bob_developer", "DevPass123!")
    if active_token:
        print(f"[+] Issued Token Vector: \n    {active_token}")

    print("\n[*] --- STEP 2: Simulating Gateway API Validation Endpoint ---")
    print("[*] Client presents token to access protected resource space...")
    claims = verify_jwt(active_token)
    if claims:
        print("[SUCCESS] API Gateway authorized request packet processing.")
        print(f"   |_ Subject: {claims['sub']} | Granted Permissions Context: {claims['role']}")

    print("\n[*] --- STEP 3: Simulating Mid-Transit Token Manipulation (Attack Check) ---")
    try:
        # Split token and manipulate payload metadata string mapping
        token_parts = active_token.split(".")
        manipulated_payload = json.loads(base64url_decode(token_parts[1]).decode("utf-8"))
        
        # Attacker tries to elevate privileges from regular context to admin authority
        manipulated_payload["role"] = "super-root-administrator"
        token_parts[1] = base64url_encode(json.dumps(manipulated_payload).encode("utf-8"))
        
        tampered_token = ".".join(token_parts)
        print(f"[!] Tampered Token Generated: \n    {tampered_token}")
        
        print("\n[*] Gateway processes tampered token payload entry...")
        audit_result = verify_jwt(tampered_token)
        if not audit_result:
            print("[+] Defense Verification Check: The system successfully denied access due to broken signature integrity.")
    except Exception as error:
        print(f"[-] Malicious extraction test terminated early: {error}")
    print("=" * 60)
