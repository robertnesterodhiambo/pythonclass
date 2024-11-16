import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set display dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced 3D Pong")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

# Define paddles and ball
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 10

# Define speeds
PADDLE_SPEED = 8
BALL_SPEED_X = 6
BALL_SPEED_Y = 4

# Define fonts
font = pygame.font.SysFont("comicsans", 50)

# Initialize the clock
clock = pygame.time.Clock()

# Define paddle and ball positions
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

ball_dx = BALL_SPEED_X * random.choice((1, -1))
ball_dy = BALL_SPEED_Y * random.choice((1, -1))

# Draw the game screen with perspective effects
def draw_window():
    WIN.fill(BLACK)

    # Simulating perspective by adjusting size based on the ball's X position (Z-axis depth effect)
    ball_distance_factor = (WIDTH // 2 - abs(WIDTH // 2 - ball.centerx)) / (WIDTH // 2)  # Simulating Z-axis

    # Simulated perspective effect for player paddle (it gets smaller with distance)
    player_paddle_width = PADDLE_WIDTH * (ball.centerx / WIDTH)
    player_paddle_height = PADDLE_HEIGHT * (ball.centerx / WIDTH)

    # Simulated perspective effect for AI paddle
    ai_paddle_width = PADDLE_WIDTH * (ball.centerx / WIDTH)
    ai_paddle_height = PADDLE_HEIGHT * (ball.centerx / WIDTH)

    # Draw the paddles with perspective effect
    pygame.draw.rect(WIN, WHITE, pygame.Rect(player_paddle.x, player_paddle.y, player_paddle_width, player_paddle_height))
    pygame.draw.rect(WIN, WHITE, pygame.Rect(ai_paddle.x, ai_paddle.y, ai_paddle_width, ai_paddle_height))

    # Ball size effect based on distance from the center
    ball_size_factor = (WIDTH // 2 - abs(WIDTH // 2 - ball.centerx)) / (WIDTH // 2)  # Simulate 3D ball size
    ball_scaled_width = BALL_RADIUS * 2 * ball_size_factor
    ball_scaled_height = BALL_RADIUS * 2 * ball_size_factor

    # Ball shading effect to simulate lighting based on distance
    ball_shade_factor = 1 - ball_distance_factor  # Darker when further away
    ball_color = (int(WHITE[0] * ball_shade_factor), int(WHITE[1] * ball_shade_factor), int(WHITE[2] * ball_shade_factor))
    
    # Draw the ball with shading
    pygame.draw.ellipse(WIN, ball_color, pygame.Rect(ball.x, ball.y, ball_scaled_width, ball_scaled_height))

    pygame.display.update()

# Move the AI paddle to follow the ball (basic AI)
def move_ai_paddle():
    if ai_paddle.centery < ball.centery and ai_paddle.bottom < HEIGHT:
        ai_paddle.y += PADDLE_SPEED
    if ai_paddle.centery > ball.centery and ai_paddle.top > 0:
        ai_paddle.y -= PADDLE_SPEED

# Check for collision with paddles
def check_collision():
    global ball_dx, ball_dy

    # Player paddle collision
    if player_paddle.colliderect(ball):
        ball_dx = -ball_dx
        ball_dy += random.randint(-5, 5)  # Add slight angle variation based on paddle hit

    # AI paddle collision
    if ai_paddle.colliderect(ball):
        ball_dx = -ball_dx
        ball_dy += random.randint(-5, 5)  # Add slight angle variation based on paddle hit

    # Ball bouncing off top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy = -ball_dy

    # Ball goes out of bounds (left or right side)
    if ball.left <= 0 or ball.right >= WIDTH:
        reset_ball()

# Reset the ball to the center
def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dx = BALL_SPEED_X * random.choice((1, -1))
    ball_dy = BALL_SPEED_Y * random.choice((1, -1))

# Handle player movement
def handle_player_movement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED

# Main game loop
def game_loop():
    global ball_dx, ball_dy
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        handle_player_movement()
        move_ai_paddle()
        ball.x += ball_dx
        ball.y += ball_dy

        check_collision()
        draw_window()

        clock.tick(60)

if __name__ == "__main__":
    game_loop()
