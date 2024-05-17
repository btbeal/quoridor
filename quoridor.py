from src.assemble_board import assemble_board_component_groups
from src.utils import display_player_walls
from src.game_display import *
from src.player import Player
from pygame.sprite import Group
from src.constants import *


class Quoridor:
    def __init__(self, players=None):
        pygame.init()
        pygame.display.set_caption("Quoridor")
        self.screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.nodes, self.walls = assemble_board_component_groups()
        if players is None:
            self.players = Quoridor.default_players()
        else:
            self.players = players
        self.player_group = Group()
        self.player_group.add(self.players)

    @staticmethod
    def default_players():
        return [
            Player(player_number=1, color=pygame.Color("coral"), position=(GAME_SIZE*0.5, HALF_DISTANCE), radius=0.5*CELL),
            Player(player_number=2, color=pygame.Color("blue"), position=(GAME_SIZE*0.5, GAME_SIZE - HALF_DISTANCE), radius=0.5*CELL)
        ]

    def play_game(self):
        current_player = 1
        while True:
            current_player_index = current_player - 1

            player = self.players[current_player_index]
            if player.is_ai:
                raise RuntimeError("AI unimplemented")
                # TODO: implement
                # while True:
                #     event = player.get_event(self.nodes, self.walls, players)
                #     if player.update(event, self.nodes, self.walls, players):
                #         break
            else:
                success = False
                while not success:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        success = player.update(event, self.nodes, self.walls, self.players)

                    self.screen.fill(WHITE)
                    self.walls.update()
                    self.walls.draw(self.screen)
                    self.nodes.draw(self.screen)
                    self.player_group.draw(self.screen)
                    display_player_walls(player_group=self.player_group, screen=self.screen, cur_play=current_player_index)
                    pygame.display.flip()


            current_player = (current_player % len(self.players)) + 1


if __name__ == '__main__':
    quoridor = Quoridor()
    quoridor.play_game()



