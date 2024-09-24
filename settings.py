import math
import pygame

pygame.init()

screen_size = pygame.display.list_modes()[0]
WIDTH, HEIGHT = screen_size
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 100
FPS_POS = (WIDTH - 65, 9)
GROUND_LEVEL = HALF_HEIGHT

MAP_SCALE = 5
MAP_TITLE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MAP_SCALE)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = DIST * TILE
SCALE = WIDTH / NUM_RAYS

player_pos = (HALF_WIDTH, HALF_HEIGHT)  # Начальная позиция игрока в центре экрана
player_angle = 0  # Начальный угол взгляда
player_speed = 1  # Скорость движения

# Определение цветов
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
SKYBLUE = (0, 106, 255)

Colores = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, BLACK, WHITE, GRAY, ORANGE, PURPLE, PINK, BROWN, SKYBLUE]