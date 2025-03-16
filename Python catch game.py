import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Object")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game variables
player_width = 50
player_height = 10
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

object_width = 30
object_height = 30
object_x = random.randint(0, WIDTH - object_width)
object_y = 0
object_speed = 5

score = 0

# Set up font
font = pygame.font.SysFont(None, 36)

# Game loop
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Move the player left and right
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Move the falling object
    object_y += object_speed
    
    # Check for collision with the player
    if (player_x < object_x + object_width and player_x + player_width > object_x and
        player_y < object_y + object_height and player_y + player_height > object_y):
        score += 1
        object_x = random.randint(0, WIDTH - object_width)
        object_y = 0
    
    # Reset object if it falls out of the screen
    if object_y > HEIGHT:
        object_x = random.randint(0, WIDTH - object_width)
        object_y = 0
    
    # Draw player
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))
    
    # Draw falling object
    pygame.draw.rect(screen, RED, (object_x, object_y, object_width, object_height))

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Update the screen
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)
