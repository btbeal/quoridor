import pygame
from src.assemble_board import assemble_board_component_groups
from src.constants import SCREEN_SIZE_X, SCREEN_SIZE_Y
from src.player import assemble_player_group
from src.utils import get_current_player
from src.game_display import text_rect, box_rect, text

nodes, walls = assemble_board_component_groups()
players = assemble_player_group()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class Quoridor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.current_player = 1

    pygame.display.set_caption("Quoridor")

    def play_game(self):
        running = True
        current_player = 1
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYDOWN:
                    current_player = 3 - current_player

            self.screen.fill(WHITE)
            curr_player = get_current_player(current_player, players)
            walls.update(events, curr_player, walls)
            players.update(events, curr_player, nodes, walls)
            walls.draw(self.screen)
            nodes.draw(self.screen)
            players.draw(self.screen)
            pygame.draw.rect(self.screen, GRAY, box_rect)
            pygame.draw.rect(self.screen, BLACK, box_rect, 2)  # Draw outline

            # Blit the text onto the screen
            screen.blit(text, text_rect)

            pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    quoridor = Quoridor()
    quoridor.play_game()


