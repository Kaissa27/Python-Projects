import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 255, 0)) # Green placeholder for ship
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH//2, SCREEN_HEIGHT-10))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        self.rect.x += direction

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill() # Removes from all groups automatically

# --- Game Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = Player()
player_group = pygame.sprite.GroupSingle(player)
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

# Create a grid of aliens
for row in range(5):
    for col in range(10):
        alien = Alien(100 + col * 60, 50 + row * 50)
        alien_group.add(alien)

# --- Main Loop ---
running = True
alien_direction = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_group.add(player.shoot())

    # Update
    player_group.update()
    bullet_group.update()
    
    # Simple Alien logic: reverse at edges
    alien_group.update(alien_direction)
    for alien in alien_group:
        if alien.rect.right >= SCREEN_WIDTH or alien.rect.left <= 0:
            alien_direction *= -1
            break

    # Collision Detection (The magic part!)
    # True, True means both the bullet and alien are destroyed on hit
    pygame.sprite.groupcollide(bullet_group, alien_group, True, True)

    # Draw
    screen.fill((0, 0, 0))
    player_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
