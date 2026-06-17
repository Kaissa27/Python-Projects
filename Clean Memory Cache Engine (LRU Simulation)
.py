from collections import OrderedDict
import time

class MemoryCacheEngine:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> int:
        if key not in self.cache:
            return -1
        # Move accessed item to the end to mark it as recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        # Evict item if storage capacity threshold is exceeded
        if len(self.cache) > self.capacity:
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)
            print(f"🧹 Storage Threshold Met. Evicted oldest cache node: [{oldest_key}]")

# Test Cache Engine
if __name__ == "__main__":
    engine = MemoryCacheEngine(capacity=3)
    engine.put("session_1", 100)
    engine.put("session_2", 200)
    engine.put("session_3", 300)
    
    engine.get("session_1") # session_1 becomes most recent
    engine.put("session_4", 400) # Evicts session_2
