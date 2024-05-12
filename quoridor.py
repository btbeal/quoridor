import pygame
from src.assemble_board import assemble_board_component_groups
from src.constants import SCREEN_SIZE_X, SCREEN_SIZE_Y, GAME_SIZE
from src.player import assemble_player_group
from src.utils import get_current_player
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
        current_player = 1
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    # At some point need to ensure event is valid
                    current_player = 3 - current_player

            self.screen.fill(WHITE)
            curr_player = get_current_player(current_player, players)

            walls.update(events, curr_player, walls)
            players.update(events, nodes, walls, current_player)

            walls.draw(self.screen)
            nodes.draw(self.screen)
            players.draw(self.screen)

            display_player_walls(player_group=players, screen=self.screen, cur_play=current_player)

            pygame.display.flip()

    pygame.quit()


def display_player_walls(player_group, screen, cur_play, font_size=18):
    my_font = pygame.font.SysFont(None, font_size)
    coordinates = {
        'player_1': {'walls_remaining': (GAME_SIZE + 20, font_size*2), 'title': (GAME_SIZE, font_size)},
        'player_2': {'walls_remaining': (GAME_SIZE + 20, font_size*4), 'title': (GAME_SIZE, font_size*3)}
    }
    for i, player in enumerate(player_group):
        text_curr_player = my_font.render(f"Curr Player: {cur_play}", False, (0, 0, 0))
        text_surface_title = my_font.render(f"Player {player.player_number}", False, (0, 0, 0))
        text_surface_walls = my_font.render(f"Total Walls {player.total_walls}", False, (0, 0, 0))
        if i == 0:
            coords = coordinates['player_1']
        else:
            coords = coordinates['player_2']
        screen.blit(text_surface_title, coords['title'])
        screen.blit(text_surface_walls, coords['walls_remaining'])
        screen.blit(text_curr_player, (100, 100))




if __name__ == '__main__':
    quoridor = Quoridor()
    quoridor.play_game()


