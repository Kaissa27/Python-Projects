import pygame
import random
import sys

pygame.init()

# 1. GRAPHICAL MATRIX CONSTRAINTS
CELL_SIZE = 12
GRID_WIDTH, GRID_HEIGHT = 70, 50
WIDTH, HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Generation Core Engine")
clock = pygame.time.Clock()

# Structural Tile Codes
TILE_WALL = 0
TILE_FLOOR = 1

# Color Profiles
COLOR_WALL = (23, 27, 36)
COLOR_FLOOR = (52, 152, 219)
COLOR_START = (46, 204, 113)

class ProceduralDungeon:
    """Manages matrix space transformations using a Drunkard's Walk algorithm."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.generate_new_map()

    def generate_new_map(self, fill_ratio=0.35):
        """Carves connected paths until a specific spatial volume is consumed."""
        # Step A: Initialize the world as solid stone mass
        self.grid = [[TILE_WALL for _ in range(self.height)] for _ in range(self.width)]
        
        # Step B: Establish starting coordinates at absolute geometric center
        self.start_x = self.width // 2
        self.start_y = self.height // 2
        
        # Current miner vector positions
        cx, cy = self.start_x, self.start_y
        self.grid[cx][cy] = TILE_FLOOR
        
        # Calculate exactly how many floor tiles we need to achieve our target layout density
        total_tiles = self.width * self.height
        target_floor_count = int(total_tiles * fill_ratio)
        current_floor_count = 1

        # Execution directional vectors mapping: Up, Down, Left, Right
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Step C: The Extraction Walker Loop
        while current_floor_count < target_floor_count:
            # Pick a completely random directional vector step
            dx, dy = random.choice(directions)
            
            # Compute new candidate location coordinates
            nx, ny = cx + dx, cy + dy
            
            # Enforce boundary safety matrices (leave a 1-tile outer perimeter wall buffer)
            if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                cx, cy = nx, ny # Move the miner
                
                # If the cell is solid wall, carve it into playable floor space
                if self.grid[cx][cy] == TILE_WALL:
                    self.grid[cx][cy] = TILE_FLOOR
                    current_floor_count += 1

    def render(self, surface):
        """Iterates through layout coordinates and draws the structural assets."""
        for x in range(self.width):
            for y in range(self.height):
                tile = self.grid[x][y]
                color = COLOR_FLOOR if tile == TILE_FLOOR else COLOR_WALL
                
                # Visual Highlight: Color the absolute starting room differently
                if x == self.start_x and y == self.start_y:
                    color = COLOR_START
                    
                pygame.draw.rect(
                    surface, 
                    color, 
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

# =====================================================================
# SYSTEM MAIN ENGINE APPLICATION
# =====================================================================
def run_application():
    dungeon = ProceduralDungeon(GRID_WIDTH, GRID_HEIGHT)
    print("🎲 Procedural Architecture Enabled. Press [SPACE] to generate a new level configuration layout.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("⚙️ Re-seeding matrix random parameters... Carving fresh level map.")
                    dungeon.generate_new_map()

        # Render the generated level geometry array directly onto the screen
        dungeon.render(screen)
        
        pygame.display.flip()
        clock.tick(30) # 30 FPS is more than sufficient for non-realtime grid maps

if __name__ == "__main__":
    run_application()
