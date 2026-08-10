import pygame
import random

pygame.init()

# Settings
WIDTH, HEIGHT = 400, 600
BIRD_SIZE = 30
PIPE_GAP = 150
PIPE_WIDTH = 60
GRAVITY = 0.5
FLAP_STRENGTH = -8
SCROLL_SPEED = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# Colors
SKY = (135, 206, 235)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

bird_x = 100
bird_y = HEIGHT // 2
bird_vel = 0

pipes = []
score = 0

def create_pipe():
    height = random.randint(100, 400)
    return {
        "x": WIDTH,
        "top": height,
        "bottom": height + PIPE_GAP
    }

pipes.append(create_pipe())

def draw_bird(x, y):
    pygame.draw.ellipse(screen, YELLOW, (x, y, BIRD_SIZE, BIRD_SIZE))
    pygame.draw.circle(screen, BLACK, (x + 22, y + 10), 3) # eye

def draw_pipe(pipe):
    # Top pipe
    pygame.draw.rect(screen, GREEN, (pipe["x"], 0, PIPE_WIDTH, pipe["top"]))
    # Bottom pipe
    pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], PIPE_WIDTH, HEIGHT))

def check_collision(bird_y, pipes):
    bird_rect = pygame.Rect(bird_x, bird_y, BIRD_SIZE, BIRD_SIZE)

    # Hit ground or ceiling
    if bird_y < 0 or bird_y > HEIGHT - BIRD_SIZE:
        return True

    for pipe in pipes:
        top_rect = pygame.Rect(pipe["x"], 0, PIPE_WIDTH, pipe["top"])
        bottom_rect = pygame.Rect(pipe["x"], pipe["bottom"], PIPE_WIDTH, HEIGHT)
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
    return False

running = True
game_over = False

while running:
    screen.fill(SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    # Reset game
                    bird_y = HEIGHT // 2
                    bird_vel = 0
                    pipes = [create_pipe()]
                    score = 0
                    game_over = False
                else:
                    bird_vel = FLAP_STRENGTH

    if not game_over:
        # Bird physics
        bird_vel += GRAVITY
        bird_y += bird_vel

        # Move pipes
        for pipe in pipes:
            pipe["x"] -= SCROLL_SPEED

        # Add new pipe
        if pipes[-1]["x"] < WIDTH - 200:
            pipes.append(create_pipe())

        # Remove pipes off screen + add score
        if pipes[0]["x"] < -PIPE_WIDTH:
            pipes.pop(0)
            score += 1

        # Check collision
        if check_collision(bird_y, pipes):
            game_over = True

    # Draw everything
    for pipe in pipes:
        draw_pipe(pipe)
    draw_bird(bird_x, bird_y)

    # Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH//2 - 50, 50))

    if game_over:
        over_text = font.render("Game Over! Press SPACE", True, BLACK)
        screen.blit(over_text, (WIDTH//2 - 120, HEIGHT//2))

    pygame.display.update()
    clock.tick(60)

pygame.quit()