import pygame 
import random 
import sys

pygame.init()

# Game Matrix Layout Settings
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = 40, 30
WIDTH, HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Architecture Matrix Snake Game")
clock = pygame.time.Clock()

# Color Codes
BG_COLOR = (26, 36, 43)
SNAKE_COLOR = (46, 204, 113)
FOOD_COLOR = (231, 76, 60)

class SnakeGameNode:
    def __init__(self):
        self.reset_state()

    def reset_state(self):
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0) # Moving right on startup
        self.spawn_food()
        self.score = 0
        self.is_game_over = False

    def spawn_food(self):
        while True:
            self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.food not in self.body: # Prevent spawning food inside the player
                break

    def change_direction(self, new_dir):
        # Prevent 180-degree self-collision turns (e.g., cannot turn left while moving right)
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def process_step_logic(self):
        if self.is_game_over:
            return

        # Calculate upcoming coordinate shift
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # EDGE WALL COLLISION CHECKS
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.is_game_over = True
            return

        # SELF-MUTILATION COLLISION CHECK
        if new_head in self.body:
            self.is_game_over = True
            return

        # Insert new head step location into array index 0
        self.body.insert(0, new_head)

        # TARGET ACQUISITION CHECK (Eating Food)
        if new_head == self.food:
            self.score += 10
            self.spawn_food()
        else:
            # If no food is eaten, drop the tail block to maintain size velocity consistency
            self.body.pop()

    def render_view(self, surface):
        surface.fill(BG_COLOR)
        
        # Render Food Vector
        pygame.draw.rect(surface, FOOD_COLOR, (self.food[0]*CELL_SIZE, self.food[1]*CELL_SIZE, CELL_SIZE-2, CELL_SIZE-2))
        
        # Render Segmented Snake Matrix
        for segment in self.body:
            pygame.draw.rect(surface, SNAKE_COLOR, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE-2, CELL_SIZE-2))

def main():
    game = SnakeGameNode()
    
    # Custom User Event ticker handling core computational ticks at 10Hz (Game Speed)
    GAME_STEP_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(GAME_STEP_EVENT, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Map keyboard inputs safely to directional coordinate changes
            elif event.type == pygame.KEYDOWN:
                if game.is_game_over and event.key == pygame.K_SPACE:
                    game.reset_state()
                elif event.key == pygame.K_UP:    game.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:  game.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:  game.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT: game.change_direction((1, 0))
                
            elif event.type == GAME_STEP_EVENT:
                game.process_step_logic()

        game.render_view(screen)
        
        if game.is_game_over:
            # Simple text message overlay when state engine sets game over
            font = pygame.font.SysFont("Arial", 24)
            msg = font.render(f"CRASH. Score: {game.score} | Press [SPACE] to restart", True, (255, 255, 255))
            screen.blit(msg, (WIDTH // 6, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
