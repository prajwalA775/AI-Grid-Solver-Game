import random
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

    def choose_move(self, target_x, target_y):
        # Simple greedy AI: move one step towards the target
        dx = 0
        dy = 0
        
        # Decide whether to prioritize moving in X or Y
        if abs(target_x - self.x) > abs(target_y - self.y):
            dx = 1 if target_x > self.x else -1
        elif abs(target_y - self.y) > 0:
            dy = 1 if target_y > self.y else -1
        else:
            dx = 1 if target_x > self.x else -1
            
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
