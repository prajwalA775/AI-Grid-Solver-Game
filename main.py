import pygame
import sys
from config import *
from game import GameState

def draw_hud(surface, font, state):
    # Health bar background
    pygame.draw.rect(surface, (100, 30, 30), (10, 10, 100, 20))
    # Health bar fill
    health_width = max(0, (state.player.health / 100) * 100)
    pygame.draw.rect(surface, (200, 30, 30), (10, 10, health_width, 20))
    
    # Hunger bar background
    pygame.draw.rect(surface, (100, 80, 20), (10, 40, 100, 20))
    # Hunger bar fill
    hunger_width = max(0, (state.player.hunger / 100) * 100)
    pygame.draw.rect(surface, (200, 150, 40), (10, 40, hunger_width, 20))
    
    # Text labels
    health_text = font.render(f"Health: {int(state.player.health)}", True, COLOR_TEXT)
    hunger_text = font.render(f"Hunger: {int(state.player.hunger)}", True, COLOR_TEXT)
    score_text = font.render(f"Score: {state.player.score}", True, COLOR_TEXT)
    
    surface.blit(health_text, (120, 10))
    surface.blit(hunger_text, (120, 40))
    surface.blit(score_text, (WINDOW_WIDTH - 150, 20))

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI Grid Survival")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16, bold=True)
    large_font = pygame.font.SysFont("Arial", 48, bold=True)
    
    state = GameState()
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and state.game_over:
                if event.key == pygame.K_r:
                    # Restart
                    state = GameState()
                    
        # Player Movement Handling
        keys = pygame.key.get_pressed()
        if not state.game_over and (current_time - state.player.last_move_time > PLAYER_TICK_MS):
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1
                
            if dx != 0 or dy != 0:
                state.player.move(dx, dy, GRID_WIDTH, GRID_HEIGHT)
                state.player.last_move_time = current_time

        # Update game state
        state.update(current_time)
        
        # Rendering
        screen.fill(COLOR_BG)
        
        # Draw grid
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))
            
        state.draw(screen)
        draw_hud(screen, font, state)
        
        if state.game_over:
            # Draw game over overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0,0))
            
            go_text = large_font.render("GAME OVER", True, (255, 100, 100))
            screen.blit(go_text, (WINDOW_WIDTH//2 - go_text.get_width()//2, WINDOW_HEIGHT//2 - 50))
            
            rst_text = font.render(f"Final Score: {state.player.score} - Press 'R' to Restart", True, COLOR_TEXT)
            screen.blit(rst_text, (WINDOW_WIDTH//2 - rst_text.get_width()//2, WINDOW_HEIGHT//2 + 20))
            
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
