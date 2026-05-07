import random
import math
from config import *

class Entity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface, pygame):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_PLAYER)
        self.health = PLAYER_START_HEALTH
        self.hunger = PLAYER_START_HUNGER
        self.score = 0
        self.last_move_time = 0

    def draw(self, surface, pygame):
        # Premium Player Look: Main body
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        
        # White inner core for "highlight"
        inner_rect = pygame.Rect(self.x * CELL_SIZE + 5, self.y * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.rect(surface, (255, 255, 255), inner_rect)
        
        # Outer glow/border
        pygame.draw.rect(surface, (100, 240, 255), rect, 2)

    def move(self, dx, dy, grid_width, grid_height):
        # Prevent moving out of bounds
        if 0 <= self.x + dx < grid_width and 0 <= self.y + dy < grid_height:
            self.x += dx
            self.y += dy

    def apply_hunger(self):
        self.hunger -= 1
        if self.hunger <= 0:
            self.hunger = 0
            self.health -= 5  # Lose health rapidly if starving

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_ENEMY)
        self.last_move_time = 0

    def draw(self, surface, pygame):
        # Pulse effect for a "premium" hostile look
        t = pygame.time.get_ticks()
        pulse = abs(int(127 * (1 + 0.5 * ( (t // 500) % 2 * 2 - 1)))) # Simple flicker/pulse
        # More elegant pulse:
        pulse_val = (math.sin(t / 200) + 1) / 2 # 0 to 1
        glow_color = (255, int(100 + 100 * pulse_val), int(100 + 100 * pulse_val))
        
        # Main body
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        
        # Dark core
        inner_rect = pygame.Rect(self.x * CELL_SIZE + 4, self.y * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(surface, (50, 0, 10), inner_rect)
        
        # Pulsing border
        pygame.draw.rect(surface, glow_color, rect, int(1 + 2 * pulse_val))

    def choose_move(self, target_x, target_y, resources=[]):
        # Ruthless pursuit: Scan for player OR nearby gold resources
        # If gold is very close, go for it to multiply!
        goal_x, goal_y = target_x, target_y
        
        nearest_gold = None
        min_dist = 8 # Scan range for gold
        
        for res in resources:
            if res.is_food:
                dist = abs(res.x - self.x) + abs(res.y - self.y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_gold = res
        
        if nearest_gold:
            goal_x, goal_y = nearest_gold.x, nearest_gold.y

        dx = 0
        dy = 0
        
        if goal_x > self.x: dx = 1
        elif goal_x < self.x: dx = -1
        
        if goal_y > self.y: dy = 1
        elif goal_y < self.y: dy = -1
            
        return dx, dy

    def move(self, dx, dy, grid_width, grid_height):
        if 0 <= self.x + dx < grid_width and 0 <= self.y + dy < grid_height:
            self.x += dx
            self.y += dy

class Resource(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_RESOURCE)
        # Type could be food or health
        self.is_food = random.choice([True, False])
        if self.is_food:
            self.color = COLOR_RESOURCE # Goldish
        else:
            self.color = (50, 250, 50) # Greenish for pure health

    def consume(self, player):
        if self.is_food:
            player.hunger += RESOURCE_HUNGER_RESTORE
            if player.hunger > 100:
                player.hunger = 100
        else:
            player.health += RESOURCE_HEALTH_RESTORE
            if player.health > 100:
                player.health = 100
        player.score += 10
