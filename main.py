import pygame
import sys
import math
from settings import *
from player import Player
from map import world_map, mini_map, generate_random_map
from ray_casting import ray_casting
from drawing import Drawing
from bullet import Bullet
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
sc_map = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
clock = pygame.time.Clock()
pitch = 0  # Vertical angle (tilt)
yaw = 0    # Horizontal angle (turn)
bullets = []
Colores = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, BLACK, WHITE, GRAY, ORANGE, PURPLE, PINK, BROWN, SKYBLUE]
show_game_menu = False  # Initialize the game menu visibility

sound_folder = os.path.join(os.path.dirname(__file__), 'sound')

# Function to check collision with walls
def check_collision(x, y):
    return any(wall_x < x < wall_x + TILE and wall_y < y < wall_y + TILE for wall_x, wall_y in world_map)

# Function to draw the main menu
def draw_main_menu(selected_item):
    sc.fill(BLACK)  # Set background color
    font = pygame.font.Font(None, 74)  # Use a large font for the menu items
    menu_items = ["Start", "Exit"]
    
    item_height = font.get_height() + 20  # Height of text + extra spacing
    total_height = len(menu_items) * item_height  # Total height of the menu
    start_y = (HEIGHT - total_height - 200) // 2  # Center vertically

    for i, item in enumerate(menu_items):
        color = YELLOW if i == selected_item else WHITE
        text = font.render(item, True, color)
        text_rect = text.get_rect(center=((WIDTH // 2) - 140, start_y + i * item_height + item_height // 2))
        sc.blit(text, text_rect)

    pygame.display.flip()

def draw_game_menu(selected_item):
    sc.fill(BLACK)  # Set background color
    font = pygame.font.Font(None, 74)  # Use a large font for the menu items
    menu_items = ["Resume", "New Game", "Exit"]
    
    item_height = font.get_height() + 20  # Height of text + extra spacing
    total_height = len(menu_items) * item_height  # Total height of the menu
    start_y = (HEIGHT - total_height - 200) // 2  # Center vertically

    for i, item in enumerate(menu_items):
        color = YELLOW if i == selected_item else WHITE
        text = font.render(item, True, color)
        text_rect = text.get_rect(center=((WIDTH // 2) - 140, start_y + i * item_height + item_height // 2))
        sc.blit(text, text_rect)

    pygame.display.flip()

# Function to handle the main menu
def main_menu():
    selected_item = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % 2  # Move up in the menu
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % 2  # Move down in the menu
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:  # Start option
                        return  # Start the game loop
                    elif selected_item == 1:  # Exit option
                        pygame.quit()
                        sys.exit()

        draw_main_menu(selected_item)

def new_game():
    global yaw, pitch, bullets, world_map, mini_map
    yaw = 0
    pitch = 0
    bullets.clear()  # Очистите список пуль

    # Генерация случайных размеров карты
    width = random.randint(15, 50)  # Ширина карты от 15 до 50 клеток
    height = random.randint(15, 50)  # Высота карты от 15 до 50 клеток
    
    # Вероятности для генерации карты
    wall_prob = random.uniform(0.2, 0.4)  # Вероятность стены от 20% до 40%
    room_prob = random.uniform(0.05, 0.15)  # Вероятность комнаты (если понадобится)
    opening_prob = random.uniform(0.1, 0.2)  # Вероятность проходов от 10% до 20%

    # Генерация случайной карты с этими параметрами
    random_map = generate_random_map(width, height, wall_prob, room_prob, opening_prob)

    # Создание мира из сгенерированной карты
    world_map = set()
    mini_map = set()
    for j, row in enumerate(random_map):
        for i, char in enumerate(row):
            if char == "W":
                world_map.add((i * TILE, j * TILE))

    # Запуск игрового цикла
    game_loop()


def game_menu():
    global show_game_menu
    show_game_menu = True  # Show the game menu when called
    selected_item = 0

    while show_game_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % 3  # Убедитесь, что здесь 3 элемента
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % 3  # Убедитесь, что здесь 3 элемента
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:  # Resume option
                        show_game_menu = False  # Exit menu and continue game
                    elif selected_item == 1:  # Новая игра
                        new_game()
                    elif selected_item == 2:  # Exit option
                        pygame.quit()
                        sys.exit()

        draw_game_menu(selected_item)

# Game loop
def game_loop():
    global yaw, pitch, bullets, os
    pygame.font.init()  # Initialize the font system
    font = pygame.font.SysFont('Arial', 30)  # Set the font and size for the ammo counter
    step_sound = pygame.mixer.Sound(os.path.join(sound_folder, "shah.wav"))
    ops_sound = pygame.mixer.Sound(os.path.join(sound_folder, "beg.wav"))
    out_of_ammo_sound = pygame.mixer.Sound(os.path.join(sound_folder, "out_of_ammo.wav"))  # Load out-of-ammo sound
    player = Player(check_collision)
    drawing = Drawing(sc)
    game_paused = False  # Flag to control the game state
    shot_tierd = 0  # Counter for shots fired
    max_shots = 5   # Maximum shots before needing to reload
    can_shoot = True  # Flag to control if the player can shoot

    screen_width = sc.get_width()

    bullet_img = pygame.image.load(os.path.join( "bullet_icon.png")).convert_alpha()  # Load bullet image
    bullet_img = pygame.transform.scale(bullet_img, (38, 38))  # Resize bullet image to 38x38

    while True:
        pygame.mouse.set_visible(False)  # Hide cursor
        pygame.event.set_grab(True)  # Lock cursor in the window

        remaining_ammo = max_shots - shot_tierd  # Calculate remaining ammo
        ammo_text = font.render(f"Ammo: {remaining_ammo}/{max_shots}", True, (255, 255, 255))  # Render ammo text (white color)

        text_rect = ammo_text.get_rect()
        text_rect.topright = (screen_width - 10, 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to toggle the game menu
                    game_menu()
                if event.key == pygame.K_r:  # Press 'R' to reload
                    shot_tierd = 0  # Reset shot counter
                    can_shoot = True  # Allow shooting again
                    out_of_ammo_sound.play()  # Play out-of-ammo sound

            if not game_paused:  # Only process input if the game is not paused
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    if can_shoot:  # Check if the player can still shoot
                        if shot_tierd < max_shots:  # Allow shooting if shot count is less than max
                            if not player.gun_sound_playing:
                                player.gun_sound.play()
                                player.shoot()
                                player.gun_sound_playing = True  # Set flag
                                bullet = Bullet(player.pos, player.angle, speed=10)  # Create bullet
                                bullets.append(bullet)  # Add bullet to the list
                                shot_tierd += 1  # Increment the shot counter
                        if shot_tierd >= max_shots:
                            can_shoot = False  # Disable shooting when max shots are reached
                            out_of_ammo_sound.play()  # Play out-of-ammo sound
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button released
                    player.gun_sound_playing = False  # Reset flag

        if game_paused:
            game_menu()  # Show the game menu if paused
            continue  # Skip the rest of the loop until the game is resumed

        mouse_x, mouse_y = pygame.mouse.get_rel()
        yaw += mouse_x * 0.1  # Turn left and right
        pitch -= mouse_y * 0.1  # Turn up and down

        # Limit the pitch angle (for example, between -90 and 90 degrees)
        pitch = max(-90, min(90, pitch))
        player.angle = math.radians(yaw)

        player.movement()
        player.update_bullets()

        for bullet in bullets:
            if bullet.update():  # If bullet should be removed
                bullets.remove(bullet)  # Remove bullet
                continue

            # Create rect for bullet
            bullet_rect = pygame.Rect(bullet.position[0], bullet.position[1], 5, 5)

        sc.fill(BLACK)
        
        drawing.background(player.crouch_height)
        drawing.world(player.pos, player.angle, player.crouch_height + player.vertical_speed)
        drawing.fps(clock)
        player.draw_bullets(sc)
        drawing.draw_mini_map(player.pos, player.angle)
        ammo_text = font.render(f"{remaining_ammo}/{max_shots}", True, (255, 255, 255))  # White color
        sc.blit(bullet_img, (screen_width - bullet_img.get_width() - 50, 10))  # Position bullet image
        sc.blit(ammo_text, (screen_width - ammo_text.get_width() - 10, 10))  # Position ammo text
        pygame.display.flip()
        clock.tick(FPS)

# Run the main menu and then the game loop
main_menu()
game_loop()