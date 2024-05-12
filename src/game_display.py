import pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
# Font settings
pygame.font.init()
font = pygame.font.Font(None, 36)


def display_game_info(players):
    for i, player in enumerate(players):
        text_surface = font.render(f"{player.player_number} Walls: {player.total_walls}", True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10 + i * 40)  # Adjust y-position for each player
        screen.blit(text_surface, text_rect)
