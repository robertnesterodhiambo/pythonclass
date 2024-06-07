import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_GAP = 5  # Space between bricks
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
MAX_BRICKS_PER_ROW = 10  # Maximum number of bricks in the top row

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cooperative Breakout Game")

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - PADDLE_HEIGHT * 2), (PADDLE_WIDTH, PADDLE_HEIGHT))
        self.speed = 10

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.velocity = [random.choice([-5, 5]), -5]

    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.velocity[0] = -self.velocity[0]
        if self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]

    def bounce(self):
        self.velocity[1] = -self.velocity[1]

# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y), (BRICK_WIDTH, BRICK_HEIGHT))

# Game setup
paddle = Paddle()
ball = Ball()
bricks = []
rows = min(MAX_BRICKS_PER_ROW, SCREEN_HEIGHT // (BRICK_HEIGHT + BRICK_GAP))

for row in range(rows):
    num_bricks = MAX_BRICKS_PER_ROW - row
    total_bricks_width = num_bricks * BRICK_WIDTH + (num_bricks - 1) * BRICK_GAP
    start_x = (SCREEN_WIDTH - total_bricks_width) // 2
    y = row * (BRICK_HEIGHT + BRICK_GAP)
    for brick in range(num_bricks):
        x = start_x + brick * (BRICK_WIDTH + BRICK_GAP)
        bricks.append(Brick(x, y))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move("left")
    if keys[pygame.K_RIGHT]:
        paddle.move("right")

    ball.move()

    # Check for collision with paddle
    if ball.rect.colliderect(paddle.rect):
        ball.bounce()

    # Check for collision with bricks
    for brick in bricks:
        if ball.rect.colliderect(brick.rect):
            ball.bounce()
            bricks.remove(brick)
            break

    # Check if ball hits the bottom
    if ball.rect.bottom >= SCREEN_HEIGHT:
        running = False

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle.rect)
    pygame.draw.ellipse(screen, WHITE, ball.rect)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick.rect)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
