import random
from settings import *

def generate_random_map(width, height, wall_prob=0.3, room_prob=0.1, opening_prob=0.15):
    text_map = []
    
    # Create a blank map with outer walls
    for y in range(height):
        row = ''
        for x in range(width):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                row += 'W'  # Outer walls
            else:
                row += '.'  # Empty space
        text_map.append(row)

    # Generate internal walls and rooms
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Randomly create walls and rooms
            if random.random() < wall_prob:
                text_map[y] = text_map[y][:x] + 'W' + text_map[y][x + 1:]

    # Create openings in walls and ensure rooms aren't closed off
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if text_map[y][x] == 'W':
                # Check adjacent cells to ensure it’s a wall and not on the border
                if random.random() < opening_prob:
                    if (text_map[y][x - 1] == '.' or text_map[y][x + 1] == '.') and \
                       (random.random() < 0.5):  # Create a horizontal opening
                        text_map[y] = text_map[y][:x] + '.' + text_map[y][x + 1:]
                    elif (text_map[y - 1][x] == '.' or text_map[y + 1][x] == '.') and \
                         (random.random() >= 0.5):  # Create a vertical opening
                        text_map[y] = text_map[y][:x] + '.' + text_map[y][x + 1:]

    # Ensure at least one entrance for each room
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if text_map[y][x] == 'W':
                if (text_map[y][x - 1] == '.' and text_map[y][x + 1] == 'W') or \
                   (text_map[y - 1][x] == '.' and text_map[y + 1][x] == 'W'):
                    text_map[y] = text_map[y][:x] + '.' + text_map[y][x + 1:]  # Ensure at least one opening

    return text_map

# Generate a random map
random_map = generate_random_map(50, 50, wall_prob=0.25, room_prob=0.15, opening_prob=0.15)

# Create world map from generated map
world_map = set()
mini_map = set()
for j, row in enumerate(random_map):
    for i, char in enumerate(row):
        if char == "W":
            world_map.add((i * TILE, j * TILE))
