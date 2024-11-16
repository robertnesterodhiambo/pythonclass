import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Constants for the game
WIDTH, HEIGHT, DEPTH = 10, 10, 10
BLOCK_SIZE = 1
SPEED = 0.2

# Directions for the snake
DIRECTIONS = {
    "UP": (0, 1, 0),
    "DOWN": (0, -1, 0),
    "LEFT": (-1, 0, 0),
    "RIGHT": (1, 0, 0),
    "FORWARD": (0, 0, 1),
    "BACKWARD": (0, 0, -1)
}

class SnakeGame3D:
    def __init__(self):
        self.snake = [(0, 0, 0)]  # Snake starts with one block
        self.direction = DIRECTIONS["UP"]
        self.food = self.place_food()
        self.score = 0
        self.game_started = False  # Flag to check if the game has started

    def place_food(self):
        while True:
            food = (random.randint(-WIDTH // 2, WIDTH // 2),
                    random.randint(-HEIGHT // 2, HEIGHT // 2),
                    random.randint(-DEPTH // 2, DEPTH // 2))
            if food not in self.snake:
                return food

    def move_snake(self):
        head = self.snake[-1]
        new_head = (head[0] + self.direction[0],
                    head[1] + self.direction[1],
                    head[2] + self.direction[2])
        
        if (new_head in self.snake or
            not (-WIDTH // 2 <= new_head[0] <= WIDTH // 2) or
            not (-HEIGHT // 2 <= new_head[1] <= HEIGHT // 2) or
            not (-DEPTH // 2 <= new_head[2] <= DEPTH // 2)):
            return False  # Game over

        self.snake.append(new_head)
        if new_head == self.food:
            self.food = self.place_food()
            self.score += 1
        else:
            self.snake.pop(0)
        
        return True

    def change_direction(self, new_direction):
        # Prevent reversing direction
        opposite = tuple(-x for x in self.direction)
        if new_direction != opposite:
            self.direction = new_direction
            self.game_started = True  # Start the game when the direction changes

    def draw_block(self, position, color):
        x, y, z = position
        glColor3f(*color)
        glPushMatrix()
        glTranslatef(x, y, z)
        glutSolidCube(BLOCK_SIZE)
        glPopMatrix()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Move camera back to view the game space
        glTranslatef(0.0, 0.0, -20)

        # Draw the snake
        for segment in self.snake:
            self.draw_block(segment, (0, 1, 0))

        # Draw the food
        self.draw_block(self.food, (1, 0, 0))

        pygame.display.flip()

def main():
    # Initialize GLUT
    glutInit()

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    game = SnakeGame3D()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game.change_direction(DIRECTIONS["UP"])
                elif event.key == pygame.K_s:
                    game.change_direction(DIRECTIONS["DOWN"])
                elif event.key == pygame.K_a:
                    game.change_direction(DIRECTIONS["LEFT"])
                elif event.key == pygame.K_d:
                    game.change_direction(DIRECTIONS["RIGHT"])
                elif event.key == pygame.K_q:
                    game.change_direction(DIRECTIONS["FORWARD"])
                elif event.key == pygame.K_e:
                    game.change_direction(DIRECTIONS["BACKWARD"])

        if game.game_started:  # Only move the snake once the game starts
            if not game.move_snake():
                print(f"Game Over! Your score: {game.score}")
                running = False

        game.render()
        clock.tick(10)  # Control game speed

    pygame.quit()

if __name__ == "__main__":
    main()
