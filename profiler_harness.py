import cProfile
import pstats
import time
import random

# =====================================================================
# 1. HEAVY MOCK GAME ENGINE SUB-SYSTEMS TO PROFILE
# =====================================================================
def simulate_quadtree_lookup():
    """Simulates a highly repeated spatial indexing check."""
    # Intentional structural slowdown: Using a non-optimized list scan 
    # instead of a true Quadtree to trigger a profile signature
    mock_entities = [{"x": random.random(), "y": random.random()} for _ in range(5000)]
    visible = []
    for ent in mock_entities:
        if 0.4 < ent["x"] < 0.6 and 0.4 < ent["y"] < 0.6:
            visible.append(ent)
    return len(visible)

def calculate_a_star_heuristics():
    """Simulates intensive pathfinding coordinate evaluation math."""
    total = 0
    # Simulating 50,000 math operations
    for _ in range(50000):
        x1, y1 = random.randint(0, 100), random.randint(0, 100)
        x2, y2 = random.randint(0, 100), random.randint(0, 100)
        total += abs(x1 - x2) + abs(y1 - y2)
    return total

def master_game_tick():
    """Executes the complete composite engine runtime stack."""
    # Simulate a standard game loop tick updating multiple systems
    simulate_quadtree_lookup()
    calculate_a_star_heuristics()
    time.sleep(0.02) # Simulating a steady 20ms physics frame cap sync

def run_heavy_simulation_loop():
    """Runs the engine continuously across 20 simulated frames."""
    print("🎮 Executing high-density simulation test bed...")
    for frame in range(20):
        master_game_tick()

# =====================================================================
# 2. THE PROFILING HOOK & ANALYSIS SYSTEM
# =====================================================================
def execute_profile_analysis():
    print("🕵️  Activating Deterministic CPU Profiler Core...")
    
    # Instantiate the native cProfile runtime capture object
    profiler = cProfile.Profile()
    
    # Start tracking CPU instructions
    profiler.enable()
    
    # Execute the primary system workload
    run_heavy_simulation_loop()
    
    # Halt instruction capture
    profiler.disable()
    
    print("\n🏁 Simulation ended. Analyzing performance statistics ledger...\n")
    
    # 3. PARSE AND FORMAT METRIC LOGS
    stats = pstats.Stats(profiler)
    
    # Sort data entries by 'cumulative' time spent inside the function
    # and print out the top 10 most expensive function calls
    stats.sort_stats(pstats.SortKey.CUMULATIVE)
    stats.print_stats(10)

if __name__ == "__main__":
    execute_profile_analysis()
