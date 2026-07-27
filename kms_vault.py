import hashlib
import secrets
import sys
import time

# --- CONFIGURATION ---
KEY_TTL_SECONDS = 5  # Key Time-To-Live in seconds (set short for demo)


class KeyManagementVault:
    """Emulates an in-memory secure vault with key rotation and token verification."""
    
    def __init__(self, key_ttl=KEY_TTL_SECONDS):
        self.key_ttl = key_ttl
        self.active_key_id = None
        self.key_store = {}  # Format: {key_id: {"key_hash": str, "created_at": float, "status": str}}

    def _hash_key(self, raw_key: str) -> str:
        """Hashes the raw key using SHA-256 so the vault never stores plaintext keys."""
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def rotate_key(self) -> str:
        """Generates a new secure API key, archives older keys, and returns the raw secret key."""
        # 1. Revoke or archive previous active key
        if self.active_key_id and self.active_key_id in self.key_store:
            self.key_store[self.active_key_id]["status"] = "ARCHIVED"

        # 2. Generate a cryptographically secure random token (URL-safe string)
        raw_secret_key = f"kms_live_{secrets.token_urlsafe(32)}"
        key_id = f"key_v{len(self.key_store) + 1}"

        # 3. Store only the hashed secret alongside metadata
        self.key_store[key_id] = {
            "key_hash": self._hash_key(raw_secret_key),
            "created_at": time.time(),
            "status": "ACTIVE"
        }
        self.active_key_id = key_id

        print(f"\033[92m[+] KMS KEY ROTATED: Created new active key [{key_id}]\033[0m")
        return raw_secret_key

    def verify_key(self, raw_key_input: str) -> tuple[bool, str]:
        """Validates an incoming API key against stored hashes and enforces TTL expiration."""
        input_hash = self._hash_key(raw_key_input)
        current_time = time.time()

        for key_id, meta in self.key_store.items():
            if meta["key_hash"] == input_hash:
                # Check if the key is explicitly archived or revoked
                if meta["status"] != "ACTIVE":
                    return False, f"KEY_REVOKED (ID: {key_id} is archived)"

                # Check if the key has exceeded its Time-To-Live (TTL)
                elapsed_time = current_time - meta["created_at"]
                if elapsed_time > self.key_ttl:
                    meta["status"] = "EXPIRED"
                    return False, f"KEY_EXPIRED (ID: {key_id} expired {elapsed_time - self.key_ttl:.1f}s ago)"

                return True, f"VALID (ID: {key_id}, TTL remaining: {self.key_ttl - elapsed_time:.1f}s)"

        return False, "INVALID_KEY (Key hash not recognized by vault)"


def run_kms_simulation():
    print("=" * 65)
    print("         KMS SECRETS VAULT & AUTOMATED KEY ROTATOR          ")
    print("=" * 65)
    print(f"[*] Initializing Secrets Vault with TTL: {KEY_TTL_SECONDS} seconds...")
    print("[*] Proving key generation, validation, and auto-rotation...\n")

    vault = KeyManagementVault(key_ttl=KEY_TTL_SECONDS)

    # 1. Initial key provisioning
    api_key_v1 = vault.rotate_key()
    print(f"   |_ Provisioned Raw Secret Key: '{api_key_v1[:20]}...'")

    # 2. Test valid key request
    print("\n--- [STAGE 1: Immediate Authentication Check] ---")
    is_valid, msg = vault.verify_key(api_key_v1)
    print(f"   |_ Result: {is_valid} | Status: {msg}")

    # 3. Wait for TTL expiration
    print(f"\n[*] Pausing execution for {KEY_TTL_SECONDS + 1} seconds to trigger TTL expiration...")
    time.sleep(KEY_TTL_SECONDS + 1)

    print("\n--- [STAGE 2: Post-TTL Authentication Check] ---")
    is_valid, msg = vault.verify_key(api_key_v1)
    print(f"\033[91m   |_ Result: {is_valid} | Status: {msg}\033[0m")

    # 4. Perform Key Rotation
    print("\n--- [STAGE 3: Key Rotation Cycle] ---")
    api_key_v2 = vault.rotate_key()
    print(f"   |_ Provisioned New Raw Secret Key: '{api_key_v2[:20]}...'")

    # Verify old key remains rejected while new key passes
    is_old_valid, old_msg = vault.verify_key(api_key_v1)
    is_new_valid, new_msg = vault.verify_key(api_key_v2)

    print(f"   |_ Old Key Status: {is_old_valid} ({old_msg})")
    print(f"\033[92m   |_ New Key Status: {is_new_valid} ({new_msg})\033[0m")

    print("=" * 65)


if __name__ == "__main__":
    try:
        run_kms_simulation()
    except KeyboardInterrupt:
        print("\n[-] KMS vault simulation stopped.")
        sys.exit(0)
