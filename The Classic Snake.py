import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Setup screen
width, height = 600, 400
screen = pygame.display.set_mode((width, height))

# Game Logic Logic
def snake_game():
    snake_pos = [[100, 50], [90, 50], [80, 50]] # Snake body segments
    food_pos = [random.randrange(1, (width//10)) * 10, 
                random.randrange(1, (height//10)) * 10]
    direction = 'RIGHT'
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: direction = 'UP'
                if event.key == pygame.K_DOWN: direction = 'DOWN'
                # (Add left/right logic here)

        # Move snake
        head = list(snake_pos[0])
        if direction == 'UP': head[1] -= 10
        if direction == 'DOWN': head[1] += 10
        # (Add left/right logic here)
        
        snake_pos.insert(0, head)
        if head == food_pos:
            food_pos = [random.randrange(1, (width//10)) * 10, 
                        random.randrange(1, (height//10)) * 10]
        else:
            snake_pos.pop()

        screen.fill((0, 0, 0)) # Clear screen
        for pos in snake_pos:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
        
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        pygame.display.flip()
        clock.tick(15) # 15 Frames per second

# snake_game()
