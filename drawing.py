import pygame
from settings import *
from ray_casting import ray_casting
from map import *
from player import *

class Drawing:
    def __init__(self, sc):
        self.sc = sc
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.pistol_image = pygame.image.load('gun.png').convert_alpha()
        self.pistol_rect = self.pistol_image.get_rect()
        self.crosshair_image = pygame.image.load('snipe.png').convert_alpha()
        self.crosshair_rect = self.crosshair_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def background(self, crouch_height):
        pygame.draw.rect(self.sc, SKYBLUE, (0, 0 - crouch_height, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.sc, GRAY, (0, HALF_HEIGHT - crouch_height, WIDTH, HALF_HEIGHT))

    def world(self, player_pos, player_angle, crouch_height):
        ray_casting(self.sc, player_pos, player_angle, crouch_height)
        self.pistol_rect.center = (player_pos[0], player_pos[1] - crouch_height)
        self.draw_pistol()
        self.draw_crosshair()

    def draw_mini_map(self, player_pos, player_angle):
        mini_map_scale = 6
        mini_map_radius = WIDTH // (3 * mini_map_scale)
        mini_map_surface = pygame.Surface((mini_map_radius * 2, mini_map_radius * 2), pygame.SRCALPHA)
        mini_map_surface.fill((0, 0, 0, 0))

        pygame.draw.circle(mini_map_surface, (30, 30, 30), (mini_map_radius, mini_map_radius), mini_map_radius)

        player_mini_x = player_pos[0] // mini_map_scale
        player_mini_y = player_pos[1] // mini_map_scale

        mini_map_offset_x = player_mini_x - mini_map_radius
        mini_map_offset_y = player_mini_y - mini_map_radius

        for wall_x, wall_y in world_map:
            mini_wall_x = (wall_x // mini_map_scale) - mini_map_offset_x
            mini_wall_y = (wall_y // mini_map_scale) - mini_map_offset_y

            if (mini_wall_x - mini_map_radius) ** 2 + (mini_wall_y - mini_map_radius) ** 2 <= (mini_map_radius - TILE // mini_map_scale) ** 2:
                pygame.draw.rect(mini_map_surface, (255, 255, 255), 
                                (mini_wall_x, mini_wall_y, TILE // mini_map_scale, TILE // mini_map_scale))

        player_circle_x = mini_map_radius
        player_circle_y = mini_map_radius
        pygame.draw.circle(mini_map_surface, (255, 0, 0), (player_circle_x, player_circle_y), 5)

        cone_length = 50
        cone_width = 20

        cone_point_x = player_circle_x + cone_length * math.cos(player_angle)
        cone_point_y = player_circle_y + cone_length * math.sin(player_angle)

        left_angle = player_angle - math.radians(cone_width / 2)
        left_x = player_circle_x + cone_length * math.cos(left_angle)
        left_y = player_circle_y + cone_length * math.sin(left_angle)

        right_angle = player_angle + math.radians(cone_width / 2)
        right_x = player_circle_x + cone_length * math.cos(right_angle)
        right_y = player_circle_y + cone_length * math.sin(right_angle)

        pygame.draw.polygon(mini_map_surface, (128, 128, 128), 
                            [(player_circle_x, player_circle_y), 
                            (left_x, left_y), 
                            (right_x, right_y)])
        
        x_offset = 20 
        y_offset = 20
        self.sc.blit(mini_map_surface, (x_offset, y_offset))

    def draw_pistol(self):
        self.pistol_rect.center = (WIDTH // 2, HEIGHT - self.pistol_rect.height // 2 - 200)
        self.sc.blit(self.pistol_image, self.pistol_rect)

    def draw_crosshair(self):
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        self.crosshair_rect.center = (center_x - 160, center_y - 20)
        self.sc.blit(self.crosshair_image, self.crosshair_rect)
        
        print(f"Crosshair center: {self.crosshair_rect.center}")

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, True, RED)
        self.sc.blit(render, FPS_POS)
