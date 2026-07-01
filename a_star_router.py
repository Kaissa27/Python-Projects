import heapq

# Directions matrix for traversing the grid (Up, Down, Left, Right)
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

class PathNode:
    """Represents a coordinate node in the pathfinding calculation space."""
    def __init__(self, x: int, y: int, g_cost: float = float('inf'), h_cost: float = 0.0, parent=None):
        self.x = x
        self.y = y
        self.g_cost = g_cost  # Cost from start node
        self.h_cost = h_cost  # Estimated cost to goal node
        self.f_cost = g_cost + h_cost  # Total cost evaluation vector
        self.parent = parent  # Link to previous node for path reconstruction

    def __lt__(self, other):
        # Overriding comparison operator so the priority queue (heap) 
        # always pops the lowest f_cost node first
        return self.f_cost < other.f_cost

def calculate_manhattan_heuristic(x1: int, y1: int, x2: int, y2: int) -> int:
    """Computes the grid-distance absolute delta baseline estimation."""
    return abs(x1 - x2) + abs(y1 - y2)

def compute_a_star_path(grid, start: tuple, goal: tuple):
    """Calculates an optimized vector node path around obstacle objects."""
    width = len(grid)
    height = len(grid[0])
    
    start_node = PathNode(start[0], start[1], g_cost=0.0, h_cost=calculate_manhattan_heuristic(start[0], start[1], goal[0], goal[1]))
    
    # Priority Queue to keep track of unvisited candidate path nodes
    open_set = []
    heapq.heappush(open_set, start_node)
    
    # Lookup dictionaries for fast structural cost inspection
    g_score_tracker = {(start[0], start[1]): 0.0}
    closed_set = set() # Nodes already processed and fully evaluated

    while open_set:
        # Pop the node with the absolute lowest f_cost
        current = heapq.heappop(open_set)
        current_coord = (current.x, current.y)

        # TARGET REACHED: Reconstruct path list by tracing parent pointers backward
        if current_coord == goal:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1] # Reverse list to get start -> goal ordering

        closed_set.add(current_coord)

        # Evaluate adjacent neighbor nodes
        for dx, dy in DIRECTIONS:
            nx, ny = current.x + dx, current.y + dy
            neighbor_coord = (nx, ny)

            # Map boundary collision checking
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            # Solid Obstacle collision validation (0 = Wall, 1 = Clear Path)
            if grid[nx][ny] == 0 or neighbor_coord in closed_set:
                continue

            # Every grid step adds an incremental cost value of 1.0
            tentative_g_score = g_score_tracker[current_coord] + 1.0

            if tentative_g_score < g_score_tracker.get(neighbor_coord, float('inf')):
                # Found a more efficient route to this neighbor node
                g_score_tracker[neighbor_coord] = tentative_g_score
                h_cost = calculate_manhattan_heuristic(nx, ny, goal[0], goal[1])
                neighbor_node = PathNode(nx, ny, g_cost=tentative_g_score, h_cost=h_cost, parent=current)
                
                heapq.heappush(open_set, neighbor_node)

    return None # Return None if no viable physical path exists

# =====================================================================
# LAYOUT SIMULATION ORCHESTRATION
# =====================================================================
def run_navigation_test():
    # 1 = Open Floor, 0 = Solid Wall Block
    # 5x5 simulation coordinate grid layout matrix
    mock_grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    
    start_point = (0, 0)
    goal_point = (4, 4)
    
    print("🧠 Initializing Informed A* Vector Path Routing Engine...")
    optimized_route = compute_a_star_path(mock_grid, start_point, goal_point)
    
    if optimized_route:
        print(f"🏁 Pathfinding Complete! Safely navigated wall matrices.")
        print(f"   Calculated Node Sequence: {optimized_route}")
    else:
        print("❌ Pathfinding Failure: Obstacles completely isolate the target point coordinates.")

if __name__ == "__main__":
    run_navigation_test()
