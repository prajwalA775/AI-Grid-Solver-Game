import random
import pygame
from config import *
from entities import Player, Enemy, Resource

class GameState:
    def __init__(self):
        self.player = Player(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.enemies = []
        self.resources = []
        
        self.last_hunger_time = pygame.time.get_ticks()
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.last_resource_spawn = pygame.time.get_ticks()
        self.game_over = False

    def get_empty_cell(self):
        # Prevent infinite loops if grid is very full, though rare in this game
        for _ in range(100):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # Check intersection
            if self.player.x == x and self.player.y == y:
                continue
            
            collision = False
            for e in self.enemies:
                if e.x == x and e.y == y:
                    collision = True
                    break
            if collision: continue
            
            for r in self.resources:
                if r.x == x and r.y == y:
                    collision = True
                    break
            if collision: continue
            
            return x, y
        return -1, -1

    def spawn_enemy(self):
        # Spawn enemy near the edges to avoid cheap hits
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = random.randint(0, GRID_WIDTH - 1), 0
        elif edge == "bottom":
            x, y = random.randint(0, GRID_WIDTH - 1), GRID_HEIGHT - 1
        elif edge == "left":
            x, y = 0, random.randint(0, GRID_HEIGHT - 1)
        else:
            x, y = GRID_WIDTH - 1, random.randint(0, GRID_HEIGHT - 1)
            
        self.enemies.append(Enemy(x, y))

    def spawn_resource(self):
        x, y = self.get_empty_cell()
        if x != -1:
            self.resources.append(Resource(x, y))

    def update(self, current_time):
        if self.game_over:
            return

        # Hunger depletion
        if current_time - self.last_hunger_time > HUNGER_DEPLETION_RATE_MS:
            self.player.apply_hunger()
            self.last_hunger_time = current_time
            if self.player.health <= 0:
                self.game_over = True

        # Enemy spawning
        if current_time - self.last_enemy_spawn > ENEMY_SPAWN_RATE_MS:
            self.spawn_enemy()
            self.last_enemy_spawn = current_time

        # Resource spawning
        if current_time - self.last_resource_spawn > RESOURCE_SPAWN_RATE_MS:
            # Keep a limit on resources so the grid doesn't fill up
            if len(self.resources) < 15:
                self.spawn_resource()
            self.last_resource_spawn = current_time

        # Enemy movement and attack logic
        for enemy in self.enemies:
            if current_time - enemy.last_move_time > ENEMY_TICK_MS:
                dx, dy = enemy.choose_move(self.player.x, self.player.y)
                
                # Check what happens if enemy moves
                nx, ny = enemy.x + dx, enemy.y + dy
                
                if nx == self.player.x and ny == self.player.y:
                    # Attack player!
                    self.player.health -= ENEMY_DAMAGE
                    if self.player.health <= 0:
                        self.game_over = True
                else:
                    # Check if valid move (not colliding with other enemies)
                    collision = False
                    for other in self.enemies:
                        if other != enemy and other.x == nx and other.y == ny:
                            collision = True
                            break
                    if not collision:
                        enemy.move(dx, dy, GRID_WIDTH, GRID_HEIGHT)
                        
                enemy.last_move_time = current_time

        # Resource collection
        for res in self.resources[:]:
            if self.player.x == res.x and self.player.y == res.y:
                res.consume(self.player)
                self.resources.remove(res)

    def draw(self, surface):
        for res in self.resources:
            res.draw(surface, pygame)
        for enemy in self.enemies:
            enemy.draw(surface, pygame)
        self.player.draw(surface, pygame)
