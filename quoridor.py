from src.assemble_board import assemble_board_component_groups
from src.constants import SCREEN_SIZE_X, SCREEN_SIZE_Y
from src.player import assemble_player_group
from src.utils import display_player_walls
from src.game_display import *

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
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            for player in players:
                success = player.update(events, nodes, walls, self.current_player)
                if success:
                    self.current_player = 3 - self.current_player
                    break

            walls.update(events, walls)
            nodes.update(events, walls)

            self.screen.fill(WHITE)
            walls.draw(self.screen)
            nodes.draw(self.screen)
            players.draw(self.screen)

            display_player_walls(player_group=players, screen=self.screen, cur_play=self.current_player)

            pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    quoridor = Quoridor()
    quoridor.play_game()


