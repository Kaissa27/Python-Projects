import pygame
import random
import sys

# Initialize
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)

snake = [[100, 50], [80, 50], [60, 50]] # list of [x, y]
direction = "RIGHT"
food = [random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)]
score = 0

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))

def show_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, [10, 10])

def game_over():
    text = font.render(f"Game Over! Score: {score}", True, RED)
    screen.blit(text, [WIDTH//3, HEIGHT//2])
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Main game loop
while True:
    screen.fill(BLACK)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction!= "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction!= "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction!= "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction!= "LEFT":
                direction = "RIGHT"

    # Move snake
    head = snake[0].copy()
    if direction == "UP": head[1] -= CELL_SIZE
    if direction == "DOWN": head[1] += CELL_SIZE
    if direction == "LEFT": head[0] -= CELL_SIZE
    if direction == "RIGHT": head[0] += CELL_SIZE
    snake.insert(0, head)

    # Check food
    if head == food:
        score += 10
        food = [random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)]
    else:
        snake.pop()

    # Check collision with walls or self
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        game_over()
    if head in snake[1:]:
        game_over()

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

    show_score()
    pygame.display.update()
    clock.tick(10) # Snake speed