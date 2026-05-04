# config.py

# Video Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
CELL_SIZE = 20

# Grid calculations
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors (Vibrant Palette)
COLOR_BG = (30, 30, 40)
COLOR_GRID = (45, 45, 55)
COLOR_PLAYER = (50, 200, 150)
COLOR_ENEMY = (220, 50, 80)
COLOR_RESOURCE = (250, 200, 50)
COLOR_TEXT = (240, 240, 240)

# Game Balance
PLAYER_START_HEALTH = 100
PLAYER_START_HUNGER = 100
HUNGER_DEPLETION_RATE_MS = 1000 # Lose 1 hunger every 1 second
RESOURCE_HUNGER_RESTORE = 20
RESOURCE_HEALTH_RESTORE = 10
ENEMY_DAMAGE = 20
ENEMY_SPAWN_RATE_MS = 3000 # Spawn an enemy every 3 seconds
RESOURCE_SPAWN_RATE_MS = 2000 # Spawn food every 2 seconds

# Action Tick Rates (Movement speed for entities on grid)
PLAYER_TICK_MS = 100 # Time between allowed player moves (faster)
ENEMY_TICK_MS = 600  # Time between enemy moves (slower)
