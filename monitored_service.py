import os
import time
import psutil
import json
from datetime import datetime
from typing import Dict, Any

class SystemTelemetryEngine:
    """Natively monitors application resource consumption and health states."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.process = psutil.Process(os.getpid())
        self.start_time = time.time()
        
    def get_uptime(self) -> float:
        return time.time() - self.start_time

    def compile_health_matrix(self, cache_status: str, db_status: str) -> Dict[str, Any]:
        """Gathers OS-level and application-level metrics into a structured telemetry frame."""
        # Query the local container or OS kernel for memory and CPU footprints
        memory_info = self.process.memory_info()
        cpu_percent = self.process.cpu_percent(interval=None)
        
        metrics_payload = {
            "telemetry_timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "service_identifier": self.service_name,
            "uptime_seconds": round(self.get_uptime(), 2),
            "hardware_allocation": {
                "cpu_utilization_pct": cpu_percent,
                "ram_resident_set_bytes": memory_info.rss,
                "ram_virtual_memory_bytes": memory_info.vms
            },
            "infrastructure_health": {
                "downstream_database": db_status,
                "redis_cache_layer": cache_status
            },
            "system_status": "HEALTHY" if db_status == "ONLINE" and cache_status == "ONLINE" else "DEGRADED"
        }
        
        return metrics_payload

# Simulating an operational loop within an enterprise service node
def run_monitored_node():
    print("🛰️ Activating Telemetry Engine Core...")
    telemetry = SystemTelemetryEngine(service_name="Ingestion_Gateway_Node_1")
    
    # Simulating standard production runtime monitoring checks
    # In a live system, these variables are derived from active network pings
    mock_redis_health = "ONLINE"
    mock_database_health = "ONLINE"
    
    for cycle in range(1, 4):
        time.sleep(1) # Simulating active request processing window
        
        # Pull live telemetric readings
        live_diagnostics = telemetry.compile_health_matrix(
            cache_status=mock_redis_health, 
            db_status=mock_database_health
        )
        
        print(f"\n📡 [Cycle {cycle}] Streaming Telemetry Frame to stdout:")
        print(json.dumps(live_diagnostics, indent=2))
        
        # Simulate a sudden downstream infrastructure event on cycle 2
        if cycle == 1:
            print("\n⚡ [ALERT] Simulating Redis memory exhaustion event...")
            mock_redis_health = "TIMEOUT_EXPIRED"

if __name__ == "__main__":
    run_monitored_node()
