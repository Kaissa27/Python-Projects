pip install cryptography

import base64
from cryptography.hazmat.primitives.asymmetric import dh, rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# --- CRYPTOGRAPHIC SETUP ---

def generate_dh_parameters():
    """Generates the shared public parameters for Diffie-Hellman."""
    print("[*] Generating Diffie-Hellman parameters (this establishes the mathematical playground)...")
    # Using 2048-bit key size for production, but using standard group for speed here
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    return parameters

def generate_rsa_keypair():
    """Generates an RSA Key Pair used for signing and authentication."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()

class NetworkEntity:
    def __init__(self, name, dh_parameters):
        self.name = name
        self.dh_parameters = dh_parameters
        # Generate Identity Keys (Asymmetric RSA)
        self.rsa_private, self.rsa_public = generate_rsa_keypair()
        # Generate Ephemeral DH Keys for key exchange
        self.dh_private = dh_parameters.generate_private_key()
        self.dh_public = self.dh_private.public_key()
        self.shared_symmetric_key = None

    def compute_shared_secret(self, peer_public_key_bytes):
        """Computes the shared secret and derives a symmetric AES key."""
        # Deserialize the peer's public key from bytes
        peer_public_key = dh.load_pem_public_key(peer_public_key_bytes)
        raw_shared_secret = self.dh_private.exchange(peer_public_key)
        
        # Derive a secure key using HKDF (Hash-based Key Derivation Function)
        self.shared_symmetric_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"handshake-derived-key",
        ).derive(raw_shared_secret)
        
        print(f"[+] {self.name} derived secure symmetric AES key: {base64.b64encode(self.shared_symmetric_key).decode()[:15]}...")

    def sign_message(self, message: bytes) -> bytes:
        """Signs a message using the entity's private RSA key."""
        signature = self.rsa_private.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_peer_signature(self, message: bytes, signature: bytes, peer_rsa_public) -> bool:
        """Verifies if a message signature matches the peer's public key."""
        try:
            peer_rsa_public.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False


# --- RUN SIMULATION ---
if __name__ == "__main__":
    print("=" * 60)
    print("      SECURE HANDSHAKE & CRYPTO SIMULATOR      ")
    print("=" * 60)

    # 1. Setup global public DH parameters
    dh_params = generate_dh_parameters()
    
    # 2. Initialize two entities (Alice and Bob)
    alice = NetworkEntity("Alice", dh_params)
    bob = NetworkEntity("Bob", dh_params)

    # 3. Serialize public keys to simulate sending over an untrusted network
    alice_dh_bytes = alice.dh_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    bob_dh_bytes = bob.dh_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    print("\n[*] --- STEP 1: Simulating Key Exchange ---")
    # Alice and Bob exchange public keys and compute the secret locally
    alice.compute_shared_secret(bob_dh_bytes)
    bob.compute_shared_secret(alice_dh_bytes)

    print("\n[*] --- STEP 2: Simulating Identity Signatures ---")
    sensitive_payload = b"CONFIDENTIAL: Target system exploitation patch applied."
    
    # Alice signs the payload using her private key to prove identity (Non-repudiation)
    alice_signature = alice.sign_message(sensitive_payload)
    print(f"[+] Alice generated RSA digital signature: {base64.b64encode(alice_signature).decode()[:20]}...")

    # 4. Bob receives the payload and verifies it came from Alice
    is_valid = bob.verify_peer_signature(sensitive_payload, alice_signature, alice.rsa_public)
    
    print(f"\n[*] --- STEP 3: Verification Result ---")
    if is_valid:
        print("[SUCCESS] Signature is VALID. The message is authentic and unaltered.")
    else:
        print("[ALERT] Signature verification FAILED! Potential tempering detected.")

    print("\n[*] --- STEP 4: Simulating a Tampering Attempt ---")
    altered_payload = b"CONFIDENTIAL: Target system exploitation patch FAILED."
    # Bob tries to verify the same signature against altered text
    is_still_valid = bob.verify_peer_signature(altered_payload, alice_signature, alice.rsa_public)
    
    if not is_still_valid:
        print("[+] Integrity check successful: The system successfully caught the altered data payload.")
    print("=" * 60)
