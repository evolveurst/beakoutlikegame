import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout")

# Set up colors
BLUE = (111, 143, 175)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
CREAM = (255, 253, 208)

# Set up the paddle
paddle_width = 100
paddle_height = 10
paddle_x = (width - paddle_width) // 2
paddle_y = height - 50
paddle_speed = 1

# Set up the ball
ball_radius = 10
ball_x = width // 2
ball_y = height // 2
ball_dx = random.choice([-2, 2])
ball_dy = -2
ball_speed = 0.09

# Set up bricks
brick_width = 75
brick_height = 20
num_bricks = 10
bricks = []
for i in range(num_bricks):
    brick_x = i * (brick_width + 10) + 35
    brick_y = 50
    bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# Set up game variables
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_speed

    # Paddle boundary check
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > width - paddle_width:
        paddle_x = width - paddle_width

    # Ball movement
    ball_x += ball_dx * ball_speed
    ball_y += ball_dy * ball_speed

    # Ball collision with walls
    if ball_x < ball_radius or ball_x > width - ball_radius:
        ball_dx *= -1
    if ball_y < ball_radius:
        ball_dy *= -1

    # Ball collision with paddle
    if ball_y > paddle_y - ball_radius:
        if paddle_x - ball_radius < ball_x < paddle_x + paddle_width + ball_radius:
            ball_dy *= -1

    # Ball collision with bricks
    for brick in bricks:
        if brick.collidepoint(ball_x, ball_y):
            bricks.remove(brick)
            ball_speed *=1.05
            ball_dy *= -1
            score += 1
            break

    # Game over condition
    if ball_y > height - ball_radius:
        lives -= 1
        if lives == 0:
            running = False
        else:
            ball_x = width // 2
            ball_y = height // 2

    # Clear the screen
    window.fill(BLACK)

    # Draw the paddle
    pygame.draw.rect(window, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))

    # Draw the ball
    pygame.draw.circle(window, PINK, (ball_x, ball_y), ball_radius)

    # Draw the bricks
    for brick in bricks:
        pygame.draw.rect(window, CYAN, brick)

    # Draw the score and lives
    score_text = font.render(f"Score: {score}", True, GREEN)
    lives_text = font.render(f"Lives: {lives}", True, CREAM)
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (width - lives_text.get_width() - 10, 10))

    # Update the display
    pygame.display.update()

# Game over message
game_over_text = font.render("Game Over", True, BLUE)
window.blit(game_over_text, ((width - game_over_text.get_width()) // 2, (height - game_over_text.get_height()) // 2))
pygame.display.update()

# Wait for a few seconds before exiting
pygame.time.wait(3000)

# Quit Pygame
pygame.quit()