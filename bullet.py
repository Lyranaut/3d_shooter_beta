import pygame
import math
from settings import *
from map import world_map

class Bullet:
    @staticmethod
    def check_collision(x, y):
        return any(wall_x < x < wall_x + TILE and wall_y < y < wall_y + TILE for wall_x, wall_y in world_map)

    def __init__(self, position, angle, speed=10, vertical_offset=-17):
        self.position = list(position)
        self.angle = angle
        self.speed = speed
        self.distance_traveled = 0
        self.max_distance = 1000
        self.angle_offset = -0.087
        self.vertical_offset = vertical_offset  # Учитываем приседание

    
    def update(self):
        adjusted_angle = self.angle + self.angle_offset
        self.position[0] += self.speed * math.cos(adjusted_angle)
        self.position[1] += self.speed * math.sin(adjusted_angle)
        self.distance_traveled += self.speed
    
        if Bullet.check_collision(self.position[0], self.position[1]):
            return True  

        if (self.position[0] < 0 or self.position[0] > WIDTH or
                self.position[1] < 0 or self.position[1] > HEIGHT):
            return True  

        return False  
    
    def draw(self, sc, player_pos, player_angle):
        rel_x = self.position[0] - player_pos[0]
        rel_y = self.position[1] - player_pos[1]

        angle_to_bullet = math.atan2(rel_y, rel_x)
        angle_diff = angle_to_bullet - player_angle

        if angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi

        bullet_y_pos = HEIGHT // 2 + int(self.vertical_offset)

        pygame.draw.circle(sc, (255, 0, 0), (WIDTH // 3 + 30, bullet_y_pos), 5)