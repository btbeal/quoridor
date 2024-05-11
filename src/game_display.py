import pygame
from src.constants import SCREEN_SIZE_X
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
# Font settings
pygame.font.init()
font = pygame.font.Font(None, 36)
text = font.render("Nice job, Player 1", True, BLACK)
text_rect = text.get_rect()

# Create a large box
box_width = 300
box_height = 100
box_rect = pygame.Rect(SCREEN_SIZE_X - box_width, 0, box_width, box_height)

# Position the text within the box
text_rect.center = box_rect.center
