import pygame
import math
from settings import *
from map import world_map

def ray_casting(sc, player_pos, player_angle, camera_height, wall_color):
    cur_angle = player_angle - HALF_FOV
    xo, yo = player_pos
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(1, MAX_DEPTH):
            x = xo + depth * cos_a
            y = yo + depth * sin_a
            if (x // TILE * TILE, y // TILE * TILE) in world_map:
                depth *= math.cos(player_angle - cur_angle)
                if depth > 0:
                    proj_height = PROJ_COEFF / depth
                    c = 255 / (1 + depth * depth * 0.00002)

                    # Используем единый цвет стен
                    pygame.draw.rect(sc, wall_color, (ray * SCALE, HALF_HEIGHT - proj_height // 2 - camera_height, SCALE, proj_height))
                break
        cur_angle += DELTA_ANGLE