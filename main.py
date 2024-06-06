import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30  # Size of each cell in the maze
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player
player_pos = [30, 30]
player_radius = 15
player_color = YELLOW
player_speed = 5

# Enemies
num_enemies = 2
enemies = []
for _ in range(num_enemies):
    enemy_pos = [random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20)]
    enemies.append(enemy_pos)
enemy_radius = 15
enemy_color = RED
enemy_speed = 5

# Maze
maze = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X............X.....X",
    "X.XXXXXXXX.X.X.X.X.X",
    "X.X....X...X.X.X.X.X",
    "X.XXX.X.XXXX.X.X.X.X",
    "X.....X.....X.X.X.X.",
    "XXXXX.X.XXXXX.X.X.X.",
    "X.....X.......X.....X",
    "XXXXX.X.XXXXXXXX.X.X",
    "X.....X.X.......X.X.X",
    "X.XXXXX.X.XXXXXXX.X.X",
    "X.X.....X.X.......X.X",
    "X.X.XXXXX.XXXXXXX.X.X",
    "X.X..............X.X",
    "X.XXXXXXXXXXXX.XXX.X",
    "X..............X...X",
    "XXXXXXXXXXXXXXXXXXXX"
]

# Pellets
pellet_points = 10
pellets = []

for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == '.':
            pellets.append((col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Game loop
run = True
score = 0
while run:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        new_pos = (player_pos[0] - player_speed, player_pos[1])
        if new_pos[0] >= 0 and (new_pos[0] // CELL_SIZE, new_pos[1] // CELL_SIZE) not in [(i, j) for j in range(len(maze)) for i in range(len(maze[j])) if maze[j][i] == 'X']:
            player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        new_pos = (player_pos[0] + player_speed, player_pos[1])
        if new_pos[0] <= WIDTH and (new_pos[0] // CELL_SIZE, new_pos[1] // CELL_SIZE) not in [(i, j) for j in range(len(maze)) for i in range(len(maze[j])) if maze[j][i] == 'X']:
            player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        new_pos = (player_pos[0], player_pos[1] - player_speed)
        if new_pos[1] >= 0 and (new_pos[0] // CELL_SIZE, new_pos[1] // CELL_SIZE) not in [(i, j) for j in range(len(maze)) for i in range(len(maze[j])) if maze[j][i] == 'X']:
            player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        new_pos = (player_pos[0], player_pos[1] + player_speed)
        if new_pos[1] <= HEIGHT and (new_pos[0] // CELL_SIZE, new_pos[1] // CELL_SIZE) not in [(i, j) for j in range(len(maze)) for i in range(len(maze[j])) if maze[j][i] == 'X']:
            player_pos[1] += player_speed

    # Handle enemies movement
    for i in range(num_enemies):
        enemy_direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])  # Random direction
        new_pos = (enemies[i][0] + enemy_direction[0] * enemy_speed, enemies[i][1] + enemy_direction[1] * enemy_speed)
        if new_pos[0] >= 0 and new_pos[0] <= WIDTH and new_pos[1] >= 0 and new_pos[1] <= HEIGHT and (new_pos[0] // CELL_SIZE, new_pos[1] // CELL_SIZE) not in [(i, j) for j in range(len(maze)) for i in range(len(maze[j])) if maze[j][i] == 'X']:
            enemies[i][0] += enemy_direction[0] * enemy_speed
            enemies[i][1] += enemy_direction[1] * enemy_speed

    # Draw everything
    win.fill(BLACK)
    # Draw maze
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 'X':
                pygame.draw.rect(win, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw pellets
    for pellet in pellets:
        pygame.draw.circle(win, WHITE, pellet, 3)
    # Draw player and enemies
    pygame.draw.circle(win, player_color, player_pos, player_radius)
    for enemy in enemies:
        pygame.draw.circle(win, enemy_color, enemy, enemy_radius)
    pygame.display.update()

    # Check for collision with enemies
    for enemy in enemies:
        if (player_pos[0] - enemy[0]) ** 2 + (player_pos[1] - enemy[1]) ** 2 <= (player_radius + enemy_radius) ** 2:
            print("Game Over")
            run = False

    # Check for collision with pellets
    for pellet in pellets:
        if (player_pos[0] - pellet[0]) ** 2 + (player_pos[1] - pellet[1]) ** 2 <= (player_radius + 3) ** 2:
            pellets.remove(pellet)
            score += pellet_points

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    win.blit(score_text, (10, 10))

    # Limit frame rate
    clock.tick(30)

pygame.quit()
