from settings import *
import pygame
import math
import os
from bullet import Bullet


sound_folder = os.path.join(os.path.dirname(__file__), 'sound')
pygame.mixer.init()


class Player:
    def __init__(self, check_collision):
        self.x, self.y = player_pos  # Стартовая позиция
        self.angle = player_angle  # Стартовый угол
        self.speed = player_speed  # Базовая скорость
        self.check_collision = check_collision
        self.crouch_height = 0
        self.vertical_speed = 0  # Вертикальная скорость
        self.on_ground = True  # Находится ли игрок на земле
        self.pistol_image = pygame.image.load('gun.png')  # Загружаем изображение
        self.pistol_rect = self.pistol_image.get_rect()  # Прямоугольник для пистолета
        # Установите позицию пистолета относительно игрока
        self.pistol_rect.center = (self.x, self.y)
        self.pitch = 0
        self.bullets = []
        self.shots_fired = 0  # Count shots fired
        self.max_shots = 5    # Maximum shots before needing to reload

        # Загрузка звуков
        self.step_sound = pygame.mixer.Sound(os.path.join(sound_folder, "shah.wav"))
        self.run_sound = pygame.mixer.Sound(os.path.join(sound_folder, "beg.wav"))
        self.gun_sound = pygame.mixer.Sound(os.path.join(sound_folder, "bang.wav"))

        # Флаги состояния игрока
        self.is_walking = False
        self.is_running = False
        self.is_shooting = False
        self.step_sound_playing = False
        self.run_sound_playing = False
        self.gun_sound_playing = False

    def shoot(self):
        bullet = Bullet(self.pos, self.angle, speed=10)  # Создаем пулю
        self.bullets.append(bullet)  # Добавляем пулю в список

    def update_bullets(self):
        for bullet in self.bullets[:]:  # Итерируем по копии списка
            if bullet.update():  # Обновляем пулю
                self.bullets.remove(bullet)

    def draw_bullets(self, sc):
        for bullet in self.bullets:
            bullet.draw(sc, self.pos, self.angle)  # Передаем позицию и угол игрока


    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self):
        keys = pygame.key.get_pressed()

        # Переменные для будущих новых позиций игрока
        new_x, new_y = self.x, self.y

        walking = False  # Инициализация переменной walking

        # Движение вперёд и назад с учётом угла взгляда
        if keys[pygame.K_w]:
            new_x += self.speed * math.cos(self.angle)
            new_y += self.speed * math.sin(self.angle)
            walking = True
        if keys[pygame.K_s]:
            new_x -= self.speed * math.cos(self.angle)
            new_y -= self.speed * math.sin(self.angle)
            walking = True

        # Движение влево и вправо
        if keys[pygame.K_a]:
            new_x -= self.speed * math.cos(self.angle + math.pi / 2)
            new_y -= self.speed * math.sin(self.angle + math.pi / 2)
            walking = True
        if keys[pygame.K_d]:
            new_x += self.speed * math.cos(self.angle + math.pi / 2)
            new_y += self.speed * math.sin(self.angle + math.pi / 2)
            walking = True

        self.base_speed = 1  # Базовая скорость

        # Проверка нажатия клавиши Shift для бега
        if keys[pygame.K_LSHIFT] and walking:  # Если игрок бежит и движется
            self.speed = self.base_speed * 2  # Увеличиваем скорость
            self.crouch_height = 0  # Игрок не может приседать при беге
            if not self.run_sound_playing:  # Если звук бега не играет
                self.run_sound.play(-1)  # Воспроизвести звук бега в цикле
                self.run_sound_playing = True
            if self.step_sound_playing:  # Останавливаем шаги, если они играли
                self.step_sound.stop()
                self.step_sound_playing = False
            self.is_running = True
            self.is_walking = False
        elif walking:  # Если игрок идёт, но не бежит
            self.speed = self.base_speed  # Обычная скорость
            if not self.step_sound_playing:  # Если звук шагов не играет
                self.step_sound.play(-1)  # Воспроизвести шаги
                self.step_sound_playing = True
            if self.run_sound_playing:  # Останавливаем бег, если он играл
                self.run_sound.stop()
                self.run_sound_playing = False
            self.is_walking = True
            self.is_running = False
        else:  # Если игрок не двигается
            if self.step_sound_playing:  # Останавливаем звук шагов
                self.step_sound.stop()
                self.step_sound_playing = False
            if self.run_sound_playing:  # Останавливаем звук бега
                self.run_sound.stop()
                self.run_sound_playing = False
            self.is_walking = False
            self.is_running = False

        if keys[pygame.K_LCTRL] and not keys[pygame.K_LALT]:  # Обычное приседание
            self.crouch_height = 50  # Смещение камеры вниз
            self.speed = self.base_speed  # Обычная скорость при приседании
            if self.run_sound_playing:
                self.run_sound.stop()
                self.run_sound_playing = False
            if self.step_sound_playing:
                self.step_sound.stop()
                self.step_sound_playing = False
        elif keys[pygame.K_LCTRL] and keys[pygame.K_LALT]:  # Приседание с Alt
            self.crouch_height = 150  # Смещение камеры вниз
            self.speed = self.base_speed  # Обычная скорость при приседании
            if self.run_sound_playing:
                self.run_sound.stop()
                self.run_sound_playing = False
            if self.step_sound_playing:
                self.step_sound.stop()
                self.step_sound_playing = False
        else:
            self.crouch_height = 0  # Обычное состояние без приседания


        # Проверка коллизий перед обновлением позиции
        if not self.check_collision(new_x, new_y):
            self.x, self.y = new_x, new_y