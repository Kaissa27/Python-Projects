# snake.py - pip install pygame
import pygame, random
pygame.init()
w, h = 600, 400
win = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

x, y = 300, 200
snake = [(x, y)]
dx, dy = 20, 0
food = (random.randrange(0,w,20), random.randrange(0,h,20))
score = 0

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP and dy==0: dx, dy = 0, -20
            if e.key == pygame.K_DOWN and dy==0: dx, dy = 0, 20
            if e.key == pygame.K_LEFT and dx==0: dx, dy = -20, 0
            if e.key == pygame.K_RIGHT and dx==0: dx, dy = 20, 0

    x += dx; y += dy
    if x<0 or x>=w or y<0 or y>=h: break
    if (x,y) in snake: break
    
    snake.append((x,y))
    if (x,y) == food:
        score+=1
        food = (random.randrange(0,w,20), random.randrange(0,h,20))
    else:
        snake.pop(0)

    win.fill((0,0,0))
    for s in snake: pygame.draw.rect(win, (0,255,0), (*s,20,20))
    pygame.draw.rect(win, (255,0,0), (*food,20,20))
    pygame.display.update()
    clock.tick(10)

print(f"Score: {score}")
pygame.quit()