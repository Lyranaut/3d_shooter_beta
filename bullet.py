import pygame
import math
from settings import *
from map import world_map

class Bullet:
    @staticmethod  # Declare this method as static
    def check_collision(x, y):
        return any(wall_x < x < wall_x + TILE and wall_y < y < wall_y + TILE for wall_x, wall_y in world_map)

    def __init__(self, position, angle, speed=10):
        self.position = list(position)  # Position of the bullet in 3D space (x, y)
        self.angle = angle  # Angle at which the bullet is fired (taken from player angle)
        self.speed = speed  # Speed of the bullet
        self.distance_traveled = 0  # Distance traveled by the bullet
        self.max_distance = 1000  # Maximum distance the bullet can travel (can be changed as desired)
        self.angle_offset = -0.087
        self.vertical_offset = -17
    
    def update(self):
        # Update the bullet position based on the firing angle
        adjusted_angle = self.angle + self.angle_offset
        self.position[0] += self.speed * math.cos(adjusted_angle)  # Movement in the X axis
        self.position[1] += self.speed * math.sin(adjusted_angle)  # Movement in the Y axis
        self.distance_traveled += self.speed
    
        if Bullet.check_collision(self.position[0], self.position[1]):  # Call as a static method
            return True  # Return True if collision occurred

        # Check if the bullet goes off-screen
        if (self.position[0] < 0 or self.position[0] > WIDTH or
                self.position[1] < 0 or self.position[1] > HEIGHT):
            return True  # Return True if the bullet went off-screen

        return False  # No collision occurred
    
    def draw(self, sc, player_pos, player_angle):
        # Convert bullet position in 3D space to 2D for drawing on screen
        rel_x = self.position[0] - player_pos[0]
        rel_y = self.position[1] - player_pos[1]
        
        # Convert bullet position to relative distance from player considering player's angle
        angle_to_bullet = math.atan2(rel_y, rel_x)
        angle_diff = angle_to_bullet - player_angle

        # Limit the angle (to keep it within -pi to pi)
        if angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi

        # Project the bullet on screen
        distance = math.hypot(rel_x, rel_y)  # Distance to the bullet
        if distance > 0:
            screen_x = WIDTH // 2 + int(angle_diff * WIDTH / FOV)  # Convert angle to screen position
            screen_y = HEIGHT // 2 - int(HEIGHT / distance)  # Convert distance to height on screen

            screen_y += self.vertical_offset
            
            # Draw the bullet
            pygame.draw.circle(sc, (255, 0, 0), (screen_x, screen_y), 5)
