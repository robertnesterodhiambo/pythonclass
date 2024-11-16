import pygame
import numpy as np
import random
import math

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 10
GRID_DEPTH = 10
BLOCK_SIZE = 30
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 165, 0)]

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('3D Tetris')

# Define shapes for Tetriminos (each shape is a list of block positions relative to (0, 0, 0))
SHAPES = [
    [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)],  # I
    [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)],  # S
    [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0)],  # L
    [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0)],  # J
    [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, -1, 0)], # T
]

# Initialize game state
grid = np.zeros((GRID_WIDTH, GRID_HEIGHT, GRID_DEPTH), dtype=int)  # 3D grid
clock = pygame.time.Clock()

# Speed control for falling blocks (lower value means faster fall)
DROP_INTERVAL = 500  # milliseconds
last_drop_time = pygame.time.get_ticks()

class Tetrimino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2
        self.y = 0
        self.z = GRID_DEPTH // 2
        self.rotation = 0  # 0: No rotation, 1: 90 degrees, etc.

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self.shape = [self.rotate_point(x, y, z) for x, y, z in self.shape]

    def rotate_point(self, x, y, z):
        if self.rotation == 1:
            return (-y, x, z)  # 90 degrees rotation around the z-axis
        elif self.rotation == 2:
            return (-x, -y, z)  # 180 degrees rotation
        elif self.rotation == 3:
            return (y, -x, z)  # 270 degrees rotation
        return (x, y, z)  # no rotation

    def move(self, dx, dy, dz):
        self.x += dx
        self.y += dy
        self.z += dz

    def get_blocks(self):
        return [(self.x + x, self.y + y, self.z + z) for x, y, z in self.shape]


def draw_grid():
    for z in range(GRID_DEPTH):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[x, y, z] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, (0, 0, 0), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)


def check_collision(tetrimino):
    for x, y, z in tetrimino.get_blocks():
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT or z < 0 or z >= GRID_DEPTH:
            return True
        if grid[x, y, z] == 1:
            return True
    return False


def place_tetrimino(tetrimino):
    for x, y, z in tetrimino.get_blocks():
        grid[x, y, z] = 1


def clear_lines():
    global grid
    for y in range(GRID_HEIGHT):
        for z in range(GRID_DEPTH):
            if all(grid[x, y, z] == 1 for x in range(GRID_WIDTH)):
                for x in range(GRID_WIDTH):
                    grid[x, y, z] = 0


def draw_tetrimino(tetrimino):
    for x, y, z in tetrimino.get_blocks():
        pygame.draw.rect(screen, tetrimino.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def main():
    global last_drop_time
    game_over = False
    current_tetrimino = Tetrimino(random.choice(SHAPES), random.choice(COLORS))

    while not game_over:
        screen.fill(BLACK)
        draw_grid()
        draw_tetrimino(current_tetrimino)

        current_time = pygame.time.get_ticks()
        
        # Check if it's time to drop the tetrimino
        if current_time - last_drop_time >= DROP_INTERVAL:
            current_tetrimino.move(0, 1, 0)
            if check_collision(current_tetrimino):
                current_tetrimino.move(0, -1, 0)
                place_tetrimino(current_tetrimino)
                clear_lines()
                current_tetrimino = Tetrimino(random.choice(SHAPES), random.choice(COLORS))
                if check_collision(current_tetrimino):
                    game_over = True
            last_drop_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetrimino.move(-1, 0, 0)
                    if check_collision(current_tetrimino):
                        current_tetrimino.move(1, 0, 0)  # Undo the move
                elif event.key == pygame.K_RIGHT:
                    current_tetrimino.move(1, 0, 0)
                    if check_collision(current_tetrimino):
                        current_tetrimino.move(-1, 0, 0)  # Undo the move
                elif event.key == pygame.K_DOWN:
                    current_tetrimino.move(0, 1, 0)
                    if check_collision(current_tetrimino):
                        current_tetrimino.move(0, -1, 0)  # Undo the move
                elif event.key == pygame.K_UP:
                    current_tetrimino.rotate()
                    if check_collision(current_tetrimino):
                        current_tetrimino.rotate()
                        current_tetrimino.rotate()
                        current_tetrimino.rotate()  # Undo rotation

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
