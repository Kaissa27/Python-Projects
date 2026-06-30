import time
from typing import Dict, Type, Any, Set

# =====================================================================
# 1. THE DATA TIER: PURE COMPONENT STORAGE STRUCTS
# =====================================================================
class Component:
    """Base structural type indicator."""
    pass

class PositionComponent(Component):
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

class VelocityComponent(Component):
    def __init__(self, vx: float = 0.0, vy: float = 0.0):
        self.vx = vx
        self.vy = vy

class RenderComponent(Component):
    def __init__(self, sprite_char: str = "·"):
        self.sprite_char = sprite_char

# =====================================================================
# 2. THE MANAGER TIER: THE CENTRAL DATABASE WAREHOUSE
# =====================================================================
class EntityManager:
    """The central state database. Tracks entities and indexes components."""
    def __init__(self):
        self.next_entity_id = 0
        # Master Dictionary: { ComponentType: { EntityID: ComponentInstance } }
        self.component_store: Dict[Type[Component], Dict[int, Component]] = {}
        
    def create_entity(self) -> int:
        entity_id = self.next_entity_id
        self.next_entity_id += 1
        return entity_id

    def add_component(self, entity_id: int, component: Component):
        comp_type = type(component)
        if comp_type not in self.component_store:
            self.component_store[comp_type] = {}
        self.component_store[comp_type][entity_id] = component

    def get_component(self, entity_id: int, comp_type: Type[Component]) -> Any:
        return self.component_store.get(comp_type, {}).get(entity_id)

    def get_entities_with_components(self, *comp_types: Type[Component]) -> Set[int]:
        """Database Index Query: Identifies entities matching the signature criteria."""
        if not comp_types:
            return set()
        
        # Start with the entity IDs that have the first component type
        result_entities = set(self.component_store.get(comp_types[0], {}).keys())
        
        # Intersect with entity IDs from the remaining component types
        for comp_type in comp_types[1:]:
            current_entities = set(self.component_store.get(comp_type, {}).keys())
            result_entities.intersection_update(current_entities)
            
        return result_entities

# =====================================================================
# 3. THE SYSTEM TIER: EXCLUSIVE ISOLATED LOGIC TRACKS
# =====================================================================
class MovementSystem:
    def update(self, entity_manager: EntityManager):
        """Processes kinematics math for entities containing Position AND Velocity."""
        # Query database for targets matching signature requirements
        target_entities = entity_manager.get_entities_with_components(PositionComponent, VelocityComponent)
        
        for entity in target_entities:
            pos = entity_manager.get_component(entity, PositionComponent)
            vel = entity_manager.get_component(entity, VelocityComponent)
            
            # Apply transformation step logic
            pos.x += vel.vx
            pos.y += vel.vy
            print(f"⚙️ [MovementSystem] Updated Entity ID [{entity}]: New Position Vector -> ({pos.x:.1f}, {pos.y:.1f})")

class RenderSystem:
    def update(self, entity_manager: EntityManager):
        """Displays items containing Position and Render descriptors."""
        target_entities = entity_manager.get_entities_with_components(PositionComponent, RenderComponent)
        
        print("\n🖼️  [RenderSystem] Rendering Frame Display State:")
        for entity in target_entities:
            pos = entity_manager.get_component(entity, PositionComponent)
            render = entity_manager.get_component(entity, RenderComponent)
            print(f"   Entity [{entity}] Drawing '{render.sprite_char}' at Coordinate Grid space ({pos.x:.1f}, {pos.y:.1f})")

# =====================================================================
# SYSTEM ENGINE ORCHESTRATOR RUNNER
# =====================================================================
def run_ecs_simulation():
    db = EntityManager()
    
    # Instantiate Systems
    movement_loop = MovementSystem()
    render_loop = RenderSystem()

    print("🚀 Initializing Decoupled Entity Component System Framework...")

    # Entity A: A moving worker node drone
    drone = db.create_entity()
    db.add_component(drone, PositionComponent(0.0, 0.0))
    db.add_component(drone, VelocityComponent(1.5, 0.5))
    db.add_component(drone, RenderComponent(sprite_char="▲"))

    # Entity B: A static telemetry beacon (Has position and look, but no movement data)
    beacon = db.create_entity()
    db.add_component(beacon, PositionComponent(10.0, 5.0))
    db.add_component(beacon, RenderComponent(sprite_char="⌖"))

    # Execute 2 ticks of our engine loop
    for tick in range(1, 3):
        print(f"\n⏱️ --- ENGINE LOOP TICK {tick} ---")
        movement_loop.update(db)
        render_loop.update(db)
        time.sleep(0.5)

if __name__ == "__main__":
    run_ecs_simulation()
