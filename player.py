from settings import *
import pygame
import math
import os
from bullet import Bullet


sound_folder = os.path.join(os.path.dirname(__file__), 'sound')
pygame.mixer.init()


class Player:
    def __init__(self, check_collision):
        self.x, self.y = player_pos 
        self.angle = player_angle 
        self.speed = player_speed 
        self.check_collision = check_collision
        self.crouch_height = 0
        self.vertical_speed = 0  
        self.on_ground = True 
        self.pistol_image = pygame.image.load('gun.png') 
        self.pistol_rect = self.pistol_image.get_rect() 
        self.pistol_rect.center = (self.x, self.y)
        self.pitch = 0
        self.bullets = []
        self.shots_fired = 0
        self.max_shots = 7

        self.step_sound = pygame.mixer.Sound(os.path.join(sound_folder, "shah.wav"))
        self.run_sound = pygame.mixer.Sound(os.path.join(sound_folder, "beg.wav"))
        self.gun_sound = pygame.mixer.Sound(os.path.join(sound_folder, "bang.wav"))

        self.is_walking = False
        self.is_running = False
        self.is_shooting = False
        self.step_sound_playing = False
        self.run_sound_playing = False
        self.gun_sound_playing = False

    def shoot(self):
        bullet = Bullet(self.pos, self.angle, speed=10)
        self.bullets.append(bullet) 

    def update_bullets(self):
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)

    def draw_bullets(self, sc):
        for bullet in self.bullets:
            bullet.draw(sc, self.pos, self.angle)


    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self):
        keys = pygame.key.get_pressed()

        new_x, new_y = self.x, self.y

        walking = False

        if keys[pygame.K_w]:
            new_x += self.speed * math.cos(self.angle)
            new_y += self.speed * math.sin(self.angle)
            walking = True
        if keys[pygame.K_s]:
            new_x -= self.speed * math.cos(self.angle)
            new_y -= self.speed * math.sin(self.angle)
            walking = True
        if keys[pygame.K_a]:
            new_x -= self.speed * math.cos(self.angle + math.pi / 2)
            new_y -= self.speed * math.sin(self.angle + math.pi / 2)
            walking = True
        if keys[pygame.K_d]:
            new_x += self.speed * math.cos(self.angle + math.pi / 2)
            new_y += self.speed * math.sin(self.angle + math.pi / 2)
            walking = True

        self.base_speed = 1

        if keys[pygame.K_LSHIFT] and walking:
            self.speed = self.base_speed * 2 
            self.crouch_height = 0
            if not self.run_sound_playing:
                self.run_sound.play(-1)
                self.run_sound_playing = True
            if self.step_sound_playing:
                self.step_sound.stop()
                self.step_sound_playing = False
            self.is_running = True
            self.is_walking = False
        elif walking:
            self.speed = self.base_speed
            if not self.step_sound_playing: 
                self.step_sound.play(-1)
                self.step_sound_playing = True
            if self.run_sound_playing:
                self.run_sound.stop()
                self.run_sound_playing = False
            self.is_walking = True
            self.is_running = False
        else:
            if self.step_sound_playing:
                self.step_sound.stop()
                self.step_sound_playing = False
            if self.run_sound_playing:
                self.run_sound.stop()
                self.run_sound_playing = False
            self.is_walking = False
            self.is_running = False

        if keys[pygame.K_LCTRL] and not keys[pygame.K_LALT]:
            self.crouch_height = 50
            self.speed = self.base_speed
            if self.run_sound_playing:
                self.run_sound.stop()
                self.run_sound_playing = False
            if self.step_sound_playing:
                self.step_sound.stop()
                self.step_sound_playing = False
        elif keys[pygame.K_LCTRL] and keys[pygame.K_LALT]:
            self.crouch_height = 150
            self.speed = self.base_speed
            if self.run_sound_playing:
                self.run_sound.stop()
                self.run_sound_playing = False
            if self.step_sound_playing:
                self.step_sound.stop()
                self.step_sound_playing = False
        else:
            self.crouch_height = 0


        if not self.check_collision(new_x, new_y):
            self.x, self.y = new_x, new_y