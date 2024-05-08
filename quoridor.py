import pygame
from src.assemble_board import assemble_board_component_groups
from src.constants import BOARD_SIZE
from src.player import assemble_player_group

nodes, walls = assemble_board_component_groups()
players = assemble_player_group()
WHITE = (255, 255, 255)


class Quoridor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
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
            walls.update(events, current_player, walls)
            players.update(events, current_player)
            walls.draw(self.screen)
            nodes.draw(self.screen)
            players.draw(self.screen)
            pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    quoridor = Quoridor()
    quoridor.play_game()


