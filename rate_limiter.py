import time
from collections import defaultdict
import sys

# --- CONFIGURATION ---
MAX_REQUESTS = 5      # Maximum requests allowed per time window
WINDOW_SIZE = 10      # Sliding window time frame (in seconds)


class SlidingWindowRateLimiter:
    def __init__(self, max_requests, window_size):
        self.max_requests = max_requests
        self.window_size = window_size
        # Dictionary storing a list of request timestamps per IP: { "IP": [timestamp1, timestamp2] }
        self.client_requests = defaultdict(list)

    def is_allowed(self, client_ip):
        """Determines if an incoming request from an IP should be allowed or throttled."""
        current_time = time.time()
        timestamps = self.client_requests[client_ip]

        # 1. Purge timestamps that fall outside the current sliding window
        while timestamps and timestamps[0] <= current_time - self.window_size:
            timestamps.pop(0)

        # 2. Check if client has exceeded the threshold
        if len(timestamps) < self.max_requests:
            timestamps.append(current_time)
            return True, len(timestamps)
        else:
            # Return False along with the time remaining until the oldest request expires
            retry_after = round(self.window_size - (current_time - timestamps[0]), 1)
            return False, retry_after


def simulate_api_traffic():
    print("=" * 60)
    print("        BASIC API RATE LIMITER & THROTTLING SIMULATOR        ")
    print("=" * 60)
    print(f"[*] Policy: Max {MAX_REQUESTS} requests per {WINDOW_SIZE}-second window.")
    print("[*] Simulating incoming API traffic...\n")

    limiter = SlidingWindowRateLimiter(max_requests=MAX_REQUESTS, window_size=WINDOW_SIZE)

    # Simulated traffic scenario from two different client IPs
    test_clients = ["192.168.1.10", "10.0.0.5"]

    # Send a burst of requests from the first IP
    print(f"--- [Traffic Burst: Client {test_clients[0]}] ---")
    for req_num in range(1, 8):
        allowed, detail = limiter.is_allowed(test_clients[0])
        
        if allowed:
            print(f"\033[92m[200 OK] Request #{req_num} allowed. (Requests in window: {detail}/{MAX_REQUESTS})\033[0m")
        else:
            print(f"\033[91m[429 TOO MANY REQUESTS] Request #{req_num} throttled! Retry after {detail}s\033[0m")
        
        time.sleep(0.5)  # Fast requests half a second apart

    # Send a single request from the second IP to prove isolation
    print(f"\n--- [Traffic Check: Independent Client {test_clients[1]}] ---")
    allowed, detail = limiter.is_allowed(test_clients[1])
    if allowed:
        print(f"\033[92m[200 OK] Request allowed for independent client {test_clients[1]}. Count: {detail}/{MAX_REQUESTS}\033[0m")

    # Wait for the sliding window to clear and test again
    print(f"\n[*] Pausing execution for {WINDOW_SIZE // 2} seconds to allow window sliding...")
    time.sleep(WINDOW_SIZE // 2)

    print(f"\n--- [Post-Cooldown Request: Client {test_clients[0]}] ---")
    allowed, detail = limiter.is_allowed(test_clients[0])
    if allowed:
        print(f"\033[92m[200 OK] Cooldown partial completion. Request allowed. Count: {detail}/{MAX_REQUESTS}\033[0m")
    else:
        print(f"\033[91m[429 TOO MANY REQUESTS] Still rate-limited. Retry after {detail}s\033[0m")

    print("=" * 60)


if __name__ == "__main__":
    try:
        simulate_api_traffic()
    except KeyboardInterrupt:
        print("\n[-] Throttling simulation terminated.")
        sys.exit(0)
