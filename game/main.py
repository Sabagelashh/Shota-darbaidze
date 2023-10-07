import pygame
from pygame.locals import *
import random
import sys

# Initialize Pygame
pygame.init()

# Define screen size and road parameters
screen_size = screen_width, screen_height = (800, 800)
road_width = int(screen_width / 1.6)
road_mark_width = int(screen_width / 80)
right_lane = screen_width / 2 + road_width / 4
left_lane = screen_width / 2 - road_width / 4

# Create the game window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Car Game")

# Load and resize shota and shaurma images
shota = pygame.image.load("shota.png")
shota = pygame.transform.scale(shota, (shota.get_width() // 2, shota.get_height() // 2))
shota_rect = shota.get_rect()
shota_rect.center = (screen_width / 2 + road_width / 4, screen_height * 0.8)

shaurma = pygame.image.load("shawarma.png")
shaurma = pygame.transform.scale(shaurma, (shaurma.get_width() // 2, shaurma.get_height() // 2))
shaurma_rect = shaurma.get_rect()
shaurma_rect.center = (screen_width / 2 - road_width / 4, screen_height * 0.2)

# Create a font for displaying messages
font = pygame.font.Font(None, 36)

# Initialize game variables
running = True
collision = False
display_message = False
score = 0
shaurma_threshold = screen_height * 0.8
counter = 0
speed = 1.0  # Initial speed

while running:
    counter += 1
    if counter == 1024:
        speed += 0.25
        counter = 0

    if not collision:
        shaurma_rect[1] += speed
        if shaurma_rect[1] > screen_height:
            shaurma_rect[1] = -200
            if random.randint(0, 1) == 0:
                shaurma_rect.center = (right_lane, -200)
            else:
                shaurma_rect.center = (left_lane, -200)

        if shaurma_rect[1] > shaurma_threshold:
            score += 1

        if shota_rect.colliderect(shaurma_rect):
            display_message = True
            collision = True

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key in [K_a, K_LEFT]:
                if shota_rect.left > (screen_width // 2 - road_width // 2 + road_mark_width):
                    shota_rect = shota_rect.move([-int(road_width / 2), 0])
            elif event.key in [K_d, K_RIGHT]:
                if shota_rect.right < (screen_width // 2 + road_width // 2 - road_mark_width * 2):
                    shota_rect = shota_rect.move([int(road_width / 2), 0])
            elif event.key == K_RETURN and display_message:
                shota_rect.center = (screen_width / 2 + road_width / 4, screen_height * 0.8)
                shaurma_rect.center = (screen_width / 2 - road_width / 4, screen_height * 0.2)
                collision = False
                display_message = False
                score = 0
                speed = 1.0  # Reset speed when the game restarts

    screen.fill((60, 220, 0))

    pygame.draw.rect(screen, (0, 0, 0), (screen_width // 2 - road_width // 2, 0, road_width, screen_height))
    pygame.draw.rect(screen, (255, 240, 60), (screen_width // 2 - road_mark_width // 2, 0, road_mark_width, screen_height))
    pygame.draw.rect(screen, (255, 255, 255), (screen_width // 2 - road_width // 2 + road_mark_width, 0, road_mark_width, screen_height))
    pygame.draw.rect(screen, (255, 255, 255), (screen_width // 2 + road_width // 2 - road_mark_width * 2, 0, road_mark_width, screen_height))

    if display_message:
        message = font.render("Game Over! Press Enter to Restart", True, (255, 0, 0))
        screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2 - message.get_height() // 2))

    score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    screen.blit(shaurma, shaurma_rect)
    screen.blit(shota, shota_rect)
    pygame.display.update()

pygame.quit()
sys.exit()
