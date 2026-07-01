from typing import List, Optional

class AxisAlignedBoundingBox:
    """Defines a structural boundary matrix for spatial checking."""
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x          # Top-left anchor X coordinate
        self.y = y          # Top-left anchor Y coordinate
        self.width = width
        self.height = height

    def contains_entity(self, ent_x: float, ent_y: float) -> bool:
        """Boundary Check: Is the specific point inside this box?"""
        return (self.x <= ent_x < self.x + self.width and
                self.y <= ent_y < self.y + self.height)

    def intersects_boundary(self, other) -> bool:
        """Collision Check: Does this bounding box overlap with another box?"""
        return not (other.x > self.x + self.width or
                    other.x + other.width < self.x or
                    other.y > self.y + self.height or
                    other.y + other.height < self.y)

class EntityProxy:
    """A minimal mock entity tracker inside our game engine space."""
    def __init__(self, entity_id: int, x: float, y: float):
        self.id = entity_id
        self.x = x
        self.y = y

class QuadtreeNode:
    """A recursive spatial node that partitions its boundary space dynamically."""
    def __init__(self, boundary: AxisAlignedBoundingBox, capacity: int = 4):
        self.boundary = boundary
        self.capacity = capacity # Max entities allowed in this node before it must split
        self.entities: List[EntityProxy] = []
        self.is_divided = False
        
        # Sub-quadrant branch references
        self.nw: Optional[QuadtreeNode] = None
        self.ne: Optional[QuadtreeNode] = None
        self.sw: Optional[QuadtreeNode] = None
        self.se: Optional[QuadtreeNode] = None

    def subdivide_space(self):
        """Splits the current node boundary matrix into four equal child quadrants."""
        sub_w = self.boundary.width / 2
        sub_h = self.boundary.height / 2
        bx, by = self.boundary.x, self.boundary.y

        self.nw = QuadtreeNode(AxisAlignedBoundingBox(bx, by, sub_w, sub_h), self.capacity)
        self.ne = QuadtreeNode(AxisAlignedBoundingBox(bx + sub_w, by, sub_w, sub_h), self.capacity)
        self.sw = QuadtreeNode(AxisAlignedBoundingBox(bx, by + sub_h, sub_w, sub_h), self.capacity)
        self.se = QuadtreeNode(AxisAlignedBoundingBox(bx + sub_w, by + sub_h, sub_w, sub_h), self.capacity)
        
        self.is_divided = True

        # Redistribution: Move current entities down into their appropriate child quadrants
        for ent in self.entities:
            self._insert_into_children(ent)
        self.entities.clear()

    def _insert_into_children(self, entity: EntityProxy) -> bool:
        """Helper to route an entity down to its correct child branch."""
        if self.nw.insert(entity): return True
        if self.ne.insert(entity): return True
        if self.sw.insert(entity): return True
        if self.se.insert(entity): return True
        return False

    def insert(self, entity: EntityProxy) -> bool:
        """Pushes an entity into the tree structure, splitting nodes on the fly if needed."""
        # 1. Reject instantly if entity point is completely outside this box boundary
        if not self.boundary.contains_entity(entity.x, entity.y):
            return False

        # 2. If already divided, bypass this node and pass entity directly to children
        if self.is_divided:
            return self._insert_into_children(entity)

        # 3. Add entity locally if capacity remains
        self.entities.append(entity)
        if len(self.entities) > self.capacity:
            self.subdivide_space()

        return True

    def query_range(self, range_box: AxisAlignedBoundingBox, found_list: List[EntityProxy]):
        """Finds all entities located inside a target search range box."""
        # Step A: Exit if the search range does not overlap with this node's box at all
        if not self.boundary.intersects_boundary(range_box):
            return

        # Step B: If this is a leaf node, check its local entities
        if not self.is_divided:
            for ent in self.entities:
                if range_box.contains_entity(ent.x, ent.y):
                    found_list.append(ent)
            return

        # Step C: If divided, recursively query all sub-quadrant branches
        self.nw.query_range(range_box, found_list)
        self.ne.query_range(range_box, found_list)
        self.sw.query_range(range_box, found_list)
        self.se.query_range(range_box, found_list)

# =====================================================================
# SYSTEM EVALUATION METRIC PERFORMANCE RUNNER
# =====================================================================
def run_spatial_benchmark():
    # Define a 1000x1000 pixel virtual game map area
    world_bounds = AxisAlignedBoundingBox(0.0, 0.0, 1000.0, 1000.0)
    tree_root = QuadtreeNode(world_bounds, capacity=4)

    print("🌲 Initializing Multi-Branch Quadtree Index Structure...")
    
    # Simulate spawning 500 entities clustered close together in a sector
    for i in range(500):
        # Placing entities near (50, 50) coordinate spaces
        ent = EntityProxy(entity_id=i, x=50.0 + (i * 0.1), y=50.0 + (i * 0.1))
        tree_root.insert(ent)

    # Define a small local physics interaction field (e.g., radius around an explosion)
    explosion_radius_box = AxisAlignedBoundingBox(45.0, 45.0, 20.0, 20.0)
    nearby_entities = []

    import time
    start_time = time.time()
    
    # Query our index
    tree_root.query_range(explosion_radius_box, nearby_entities)
    
    elapsed = (time.time() - start_time) * 1000

    print(f"🏁 Spatial Lookup Complete in {elapsed:.4f}ms!")
    print(f"   Pruned search space down from 500 records to checking just {len(nearby_entities)} candidate objects.")
    print(f"   Target Entity IDs matched in zone: {[e.id for e in nearby_entities[:5]]}...")

if __name__ == "__main__":
    run_spatial_benchmark()
