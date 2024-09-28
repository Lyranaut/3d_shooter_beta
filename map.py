import random
from settings import *

# Define multiple colors for the walls
WALL_COLORS = [
    (139, 69, 19),  # Brown
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (255, 192, 203) # Pink
]

# Define color for empty spaces
EMPTY_COLOR = (255, 255, 255)  # White color for empty spaces

def generate_random_map(width, height, wall_prob=0.15, room_prob=0.15, opening_prob=0.15):
    text_map = []
    
    # Create an empty map with outer walls
    for y in range(height):
        row = []
        for x in range(width):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                row.append(('W', random.choice(WALL_COLORS)))  # Outer walls with random color
            else:
                row.append(('.', EMPTY_COLOR))  # Empty space
        text_map.append(row)

    # Generate larger rooms
    for _ in range(5):  # Create 5 rooms
        room_width = random.randint(5, 10)  # Increase room size
        room_height = random.randint(5, 10)  # Increase room size
        room_x = random.randint(1, width - room_width - 1)
        room_y = random.randint(1, height - room_height - 1)
        
        # Ensure the room does not overlap existing walls
        if all(text_map[y][x][0] == '.' for y in range(room_y, room_y + room_height) 
                                                   for x in range(room_x, room_x + room_width)):
            # Create room
            for y in range(room_y, room_y + room_height):
                for x in range(room_x, room_x + room_width):
                    text_map[y][x] = ('.', EMPTY_COLOR)  # Empty space for the room
            
            # Create entrance (one entrance per room)
            entrance_x = random.randint(room_x, room_x + room_width - 1)
            entrance_y = room_y + room_height  # Entrance below the room
            if entrance_y < height - 1 and text_map[entrance_y][entrance_x][0] == '.':
                text_map[entrance_y][entrance_x] = ('.', EMPTY_COLOR)

    # Generate walls while avoiding single walls
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Randomly create walls
            if random.random() < wall_prob and text_map[y][x][0] == '.':
                # Check surrounding tiles to avoid creating single walls
                if (text_map[y-1][x][0] == 'W' and text_map[y+1][x][0] == 'W' and
                    text_map[y][x-1][0] == '.' and text_map[y][x+1][0] == '.'):
                    continue  # Skip to avoid single wall

                if (text_map[y][x-1][0] == 'W' and text_map[y][x+1][0] == 'W' and
                    text_map[y-1][x][0] == '.' and text_map[y+1][x][0] == '.'):
                    continue  # Skip to avoid single wall

                # Place a wall with a random color
                text_map[y][x] = ('W', random.choice(WALL_COLORS))

    # Create openings in walls
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if text_map[y][x][0] == 'W':
                if random.random() < opening_prob:
                    if (text_map[y][x - 1][0] == '.' or text_map[y][x + 1][0] == '.') and (random.random() < 0.5):  # Create horizontal opening
                        text_map[y][x] = ('.', EMPTY_COLOR)
                    elif (text_map[y - 1][x][0] == '.' or text_map[y + 1][x][0] == '.') and (random.random() >= 0.5):  # Create vertical opening
                        text_map[y][x] = ('.', EMPTY_COLOR)

    return text_map

# Generate a random map
random_map = generate_random_map(50, 50, wall_prob=0.15, room_prob=0.15, opening_prob=0.15)

# Create the world map from the generated map
world_map = set()
mini_map = set()
for j, row in enumerate(random_map):
    for i, (char, color) in enumerate(row):
        if char in "W|":  # Solid wall and wall with window
            world_map.add((i * TILE, j * TILE))
