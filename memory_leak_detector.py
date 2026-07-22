import gc 
import objgraph

# =====================================================================
# 1. THE ARCHITECTURAL LEAK SIMULATION
# =====================================================================
class GameComponent:
    """A data component attached to an entity."""
    def __init__(self, name: str):
        self.name = name

class LeakySystem:
    """Simulates an engine system that accidentally leaks reference tracks."""
    def __init__(self):
        # The leak source: A global audit ledger that never cleans itself up
        self.leaked_references_ledger = []

    def spawn_and_destroy_entities(self):
        print("⚡ Spawning 1000 temporary entities into runtime memory...")
        for i in range(1000):
            comp = GameComponent(name=f"Particle_{i}")
            
            # ACCIDENTAL REFERENCE CAPTURE: 
            # We append the component to our global tracking ledger. 
            # Even when this loop ends and the local variable scope drops, 
            # the ledger keeps the object alive in RAM!
            self.leaked_references_ledger.append(comp)
            
        print("🗑️  Local variables dropped out of frame scope.")

# =====================================================================
# 2. THE INFRASTRUCTURE MEMORY AUDIT HOOK
# =====================================================================
def run_memory_leak_audit():
    print("🕵️  Activating Native Object Lifetime Memory Tracker...")
    
    # Ensure the Garbage Collector is completely clean before starting our test
    gc.collect()
    
    # Take an initial baseline count of how many GameComponent instances exist in RAM
    initial_count = objgraph.count('GameComponent')
    print(f"📊 Baseline RAM State: Existing GameComponent instances = {initial_count}")

    # Trigger our simulation loop
    system_node = LeakySystem()
    system_node.spawn_and_destroy_entities()

    # Explicitly invoke Python's Garbage Collection sweep manually
    print("🧹 Triggering manual garbage collection pass...")
    gc.collect()

    # Re-evaluate the object count in memory
    post_cleanup_count = objgraph.count('GameComponent')
    print(f"📊 Post-Collection RAM State: Existing GameComponent instances = {post_cleanup_count}")

    # 3. DIAGNOSTIC INTERROGATION LAYER
    if post_cleanup_count > initial_count:
        print(f"\n🚨 [CRITICAL MEMORY LEAK DETECTED]: {post_cleanup_count - initial_count} objects leaked!")
        
        # Pull the first leaked instance from memory
        leaked_objects = objgraph.by_type('GameComponent')
        sample_leak = leaked_objects[0]
        
        print("\n🔍 Traceback: Finding the chain of variables keeping this object alive:")
        # Print the backreference chain to stdout showing exactly who points to the leak
        objgraph.show_backrefs([sample_leak], max_depth=3, filename='memory_leak_graph.png')
        print("📁 Memory reference map exported to 'memory_leak_graph.png'.")
        
        # Text-based breakdown summary of what holds the leak reference
        print(f"   The leaked object is referenced directly by: {objgraph.find_backref_chain(sample_leak, objgraph.is_proper_module)}")

if __name__ == "__main__":
    run_memory_leak_audit()
