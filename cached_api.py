import json
import time
import pandas as pd
import redis
from fastapi import FastAPI, HTTPException
from pathlib import Path

app = FastAPI(title="Enterprise Cache-Optimized Analytics API")

# 1. ESTABLISH RAM CACHE CONNECTION CONNECTION
# Connects directly to our in-memory Redis instance
redis_client = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)

CACHE_KEY_ANALYTICS = "dashboard:regional_revenue"
CACHE_TTL_SECONDS = 60 # Data will stay in memory for exactly 1 minute before expiring

# Helper variable to simulate an expensive database table scan computation
MOCK_DATABASE_LOGS = {
    "region": ["US-East", "US-West", "EU-West", "APAC-South"],
    "aggregated_revenue": [45000.80, 89000.20, 120400.50, 31000.10]
}

# =====================================================================
# 2. HIGH-PERFORMANCE CACHED READ ENDPOINT
# =====================================================================
@app.get("/analytics/revenue")
def get_regional_revenue_report():
    """Fetches complex analytical frameworks using an in-memory cache architecture."""
    start_time = time.time()
    
    # STEP A: Intercept and query the in-memory cache engine first
    try:
        cached_data = redis_client.get(CACHE_KEY_ANALYTICS)
    except redis.RedisError as e:
        print(f"⚠️ Redis connection offline: {e}")
        cached_data = None

    # STEP B: CACHE HIT - Data found in RAM! Return it instantly.
    if cached_data:
        elapsed = (time.time() - start_time) * 1000 # Convert to milliseconds
        # Unpack the string back into standard JSON arrays
        report_data = json.loads(cached_data)
        return {
            "source": "Redis Memory Cache (Cache Hit)",
            "execution_speed": f"{elapsed:.3f}ms",
            "data": report_data
        }

    # STEP C: CACHE MISS - Data not found. Hit the heavy core database.
    print("🔍 Cache Miss! Pulling record matrices from physical database layers...")
    
    # Simulating a heavy SQL query execution delay (e.g., millions of rows calculated)
    time.sleep(1.2) 
    df = pd.DataFrame(MOCK_DATABASE_LOGS)
    report_json_string = df.to_json(orient="records")
    
    # STEP D: WRITE BACK TO CACHE - Save results to RAM with an expiration timer
    try:
        # ex=CACHE_TTL_SECONDS sets the time-to-live. It vanishes automatically in 60s.
        redis_client.set(CACHE_KEY_ANALYTICS, report_json_string, ex=CACHE_TTL_SECONDS)
    except redis.RedisError as e:
        print(f"⚠️ Failed to write to Redis memory ledger: {e}")

    elapsed = (time.time() - start_time) * 1000
    return {
        "source": "Core Database Engine (Cache Miss)",
        "execution_speed": f"{elapsed:.3f}ms",
        "data": json.loads(report_json_string)
    }

# =====================================================================
# 3. CACHE INVALIDATION ENDPOINT (The Cleanup System)
# =====================================================================
@app.post("/analytics/invalidate")
def force_refresh_cache():
    """Forces the system to delete the cache if new entries are written to the DB."""
    redis_client.delete(CACHE_KEY_ANALYTICS)
    return {"status": "success", "message": "Memory cache cleared. Next read will hit the database fresh."}

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    pass
