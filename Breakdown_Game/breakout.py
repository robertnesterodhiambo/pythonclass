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
BRICK_SCORE = 8
MAX_LEVEL = 5  # Maximum number of levels

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Create the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cooperative Breakout Game")

# Create two surfaces for game area and info panel
game_surface = pygame.Surface((SCREEN_WIDTH - 200, SCREEN_HEIGHT))  # Game panel surface
info_surface = pygame.Surface((200, SCREEN_HEIGHT))  # Information panel surface

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - PADDLE_HEIGHT * 2), (PADDLE_WIDTH, PADDLE_HEIGHT))
        self.speed = 10

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < SCREEN_WIDTH - 200:  # Adjusted for panel width
            self.rect.x += self.speed

# Ball class
class Ball:
    def __init__(self, level):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.velocity = [random.choice([-5, 5]), -5]
        self.speed = 5 + level  # Initial speed increases with level

    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH - 200:  # Adjusted for panel width
            self.velocity[0] = -self.velocity[0]
        if self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]

    def bounce(self):
        self.velocity[1] = -self.velocity[1]

    def reset(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.velocity = [random.choice([-5, 5]), -5]
        self.speed += 1  # Increase speed when resetting ball

# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y), (BRICK_WIDTH, BRICK_HEIGHT))

# Function to create bricks for a given level
def create_bricks(level):
    bricks = []
    if level == 1:
        num_bricks = 4  # Start with 4 bricks for Level 1
    else:
        num_rows = min(3 + level, 6)  # Increase rows as level progresses, capped at 6
        num_bricks = 8 + level * 2  # Increase bricks per level
    
    for row in range(3):
        for col in range(num_bricks):
            x = col * (BRICK_WIDTH + BRICK_GAP) + 50
            y = row * (BRICK_HEIGHT + BRICK_GAP) + 50
            bricks.append(Brick(x, y))
    return bricks

# Initialize game objects
paddle = Paddle()
level = 1  # Start at level 1
lives = 3
score = 0

# Font for displaying text
font = pygame.font.SysFont(None, 30)

# Function to draw game information panel
def draw_info_panel(level, lives, score, player_name):
    info_surface.fill(BLACK)
    text_level = font.render(f"Level: {level}", True, WHITE)
    text_lives = font.render(f"Lives: {lives}", True, WHITE)
    text_score = font.render(f"Score: {score}", True, WHITE)
    text_player = font.render(f"Player: {player_name}", True, WHITE)
    info_surface.blit(text_level, (20, 50))
    info_surface.blit(text_lives, (20, 100))
    info_surface.blit(text_score, (20, 150))
    info_surface.blit(text_player, (20, 200))
    
    # Show top 10 scores
    try:
        rank_text = font.render("Top 10 Players", True, WHITE)
        info_surface.blit(rank_text, (20, 250))
        
        with open("scores.txt", "r") as rank_file:
            lines = rank_file.readlines()
            
        y_offset = 280
        for i, line in enumerate(lines[:10]):
            try:
                name, score = line.strip().split(",")
                rank_entry = font.render(f"{i + 1}. {name}: {score}", True, WHITE)
                info_surface.blit(rank_entry, (20, y_offset))
                y_offset += 30
            except ValueError:
                print(f"Skipping line {i + 1} in scores.txt due to incorrect format.")
                continue

    except FileNotFoundError:
        print("scores.txt not found.")
        pass

# Function to update and store scores
def update_scores(player_name, player_score):
    try:
        # Read current scores
        scores = []
        with open("scores.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                name, score = line.strip().split(",")
                scores.append((name, int(score)))
        
        # Add current player's score
        scores.append((player_name, player_score))
        
        # Sort scores by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Keep only top 10 scores
        top_scores = scores[:10]
        
        # Write back to file
        with open("scores.txt", "w") as file:
            for name, score in top_scores:
                file.write(f"{name},{score}\n")
    
    except FileNotFoundError:
        # Create the file if it doesn't exist
        with open("scores.txt", "w") as file:
            file.write(f"{player_name},{player_score}\n")

# Main game loop
def main_game(player_name):
    global paddle, ball, level, lives, score

    running = True
    while running:
        if level > MAX_LEVEL:
            break
        
        # Create bricks for the current level
        bricks = create_bricks(level)

        # Initialize ball
        ball = Ball(level)
        ball.reset()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

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
            for brick in bricks[:]:  # Iterate over a copy to allow removal
                if ball.rect.colliderect(brick.rect):
                    ball.bounce()
                    bricks.remove(brick)
                    score += BRICK_SCORE

            # Check if ball hits the bottom
            if ball.rect.bottom >= SCREEN_HEIGHT:
                lives -= 1
                if lives > 0:
                    ball.reset()
                else:
                    update_scores(player_name, score)
                    running = False
                    break

            # Check if all bricks are removed
            if not bricks:
                level += 1
                break

            # Drawing
            screen.fill(BLACK)

            # Draw game area
            pygame.draw.rect(screen, BLUE, paddle.rect)
            pygame.draw.ellipse(screen, WHITE, ball.rect)
            for brick in bricks:
                pygame.draw.rect(screen, RED, brick.rect)

            # Draw info panel
            screen.blit(info_surface, (SCREEN_WIDTH - 200, 0))
            draw_info_panel(level, lives, score, player_name)

            pygame.display.flip()
            pygame.time.delay(30)

    # Game over, update high scores, etc.
    pygame.quit()

# Entry point
if __name__ == "__main__":
    # Request player's name from UI (you need to implement this part)
    player_name = input("Enter your name: ")  # Replace with UI input

    # Run the main game loop
    main_game(player_name)
