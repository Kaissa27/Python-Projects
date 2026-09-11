pip install pygame numpy

import pygame
import random
import numpy as np
from collections import deque

# --- GAME SETTINGS ---
WIDTH, HEIGHT = 400, 400
GRID = 20
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- AI AGENT - Q-LEARNING TABLE ---
class QAgent:
    def __init__(self):
        self.q_table = {} # state -> [up, down, left, right] values
        self.lr = 0.1
        self.gamma = 0.9
        self.epsilon = 1.0 # start with 100% random
        self.epsilon_decay = 0.9995

    def get_state(self, snake, food, direction):
        # State = Where is food compared to head + danger around
        head_x, head_y = snake[-1]
        food_x, food_y = food

        # 1=food is there, 0=not
        food_up = 1 if food_y < head_y else 0
        food_down = 1 if food_y > head_y else 0
        food_left = 1 if food_x < head_x else 0
        food_right = 1 if food_x > head_x else 0

        # Danger detection
        danger_up = 1 if (head_x, head_y-GRID) in snake or head_y-GRID < 0 else 0
        danger_down = 1 if (head_x, head_y+GRID) in snake or head_y+GRID >= HEIGHT else 0
        danger_left = 1 if (head_x-GRID, head_y) in snake or head_x-GRID < 0 else 0
        danger_right = 1 if (head_x+GRID, head_y) in snake or head_x+GRID >= WIDTH else 0

        state = (food_up, food_down, food_left, food_right, danger_up, danger_down, danger_left, danger_right, direction)
        return state

    def get_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0,0,0,0] # up, down, left, right

        if random.random() < self.epsilon:
            return random.randint(0,3) # explore
        else:
            return np.argmax(self.q_table[state]) # exploit - best move

    def train(self, state, action, reward, next_state):
        if state not in self.q_table: self.q_table[state] = [0,0,0,0]
        if next_state not in self.q_table: self.q_table[next_state] = [0,0,0,0]

        # Q-Learning Formula: Q = Q + lr*(reward + gamma*max_next_Q - Q)
        old_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state])
        new_q = old_q + self.lr * (reward + self.gamma * max_next_q - old_q)
        self.q_table[state][action] = new_q

        if self.epsilon > 0.01:
            self.epsilon *= self.epsilon_decay

# --- GAME LOOP WITH AI ---
agent = QAgent()
snake = [(200,200)]
direction = 0 # 0=up,1=down,2=left,3=right
food = (random.randrange(0,WIDTH,GRID), random.randrange(0,HEIGHT,GRID))
score = 0
episode = 0

# For Streamlit-style stats
scores_history = []

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False

    # AI decides
    state = agent.get_state(snake, food, direction)
    action = agent.get_action(state)

    # Prevent reverse
    if (direction==0 and action==1) or (direction==1 and action==0) or (direction==2 and action==3) or (direction==3 and action==2):
        action = direction
    else:
        direction = action

    # Move snake
    head_x, head_y = snake[-1]
    if direction == 0: head_y -= GRID
    if direction == 1: head_y += GRID
    if direction == 2: head_x -= GRID
    if direction == 3: head_x += GRID

    new_head = (head_x, head_y)

    # Reward system
    reward = 0
    done = False

    if head_x<0 or head_x>=WIDTH or head_y<0 or head_y>=HEIGHT or new_head in snake:
        reward = -100 # died
        done = True
    elif new_head == food:
        reward = 100 # ate food
        score += 1
        food = (random.randrange(0,WIDTH,GRID), random.randrange(0,HEIGHT,GRID))
        snake.append(new_head)
    else:
        # Small reward if getting closer to food
        old_dist = abs(snake[-1][0]-food[0]) + abs(snake[-1][1]-food[1])
        new_dist = abs(new_head[0]-food[0]) + abs(new_head[1]-food[1])
        reward = 1 if new_dist < old_dist else -1
        snake.append(new_head)
        snake.pop(0)

    next_state = agent.get_state(snake, food, direction)
    agent.train(state, action, reward, next_state)

    # Draw
    win.fill((0,0,0))
    for s in snake: pygame.draw.rect(win, (0,255,0), (*s,GRID,GRID))
    pygame.draw.rect(win, (255,0,0), (*food,GRID,GRID))
    pygame.display.set_caption(f"Episode: {episode} | Score: {score} | Epsilon: {agent.epsilon:.2f}")
    pygame.display.update()
    clock.tick(60) # Fast training

    if done:
        scores_history.append(score)
        if len(scores_history) % 10 == 0:
            print(f"Episode {len(scores_history)} - Avg Score last 10: {np.mean(scores_history[-10:]):.2f} - Epsilon: {agent.epsilon:.2f}")
        snake = [(200,200)]
        direction = 0
        score = 0
        episode += 1

pygame.quit()
print("Training Complete! Q-Table size:", len(agent.q_table))