from src.assemble_board import assemble_board_component_groups
from src.player import Player
from pygame.sprite import Group
from src.constants import *
import pygame

DEFAULT_FONT_SIZE = 32


class Quoridor:
    def __init__(self, players=None, font_size=DEFAULT_FONT_SIZE):
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
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, font_size)

    @staticmethod
    def default_players():
        return [
            Player(name="Player 1", color=pygame.Color("coral"), position=(GAME_SIZE*0.5, HALF_DISTANCE), radius=0.5*CELL),
            Player(name="Player 2", color=pygame.Color("blue"), position=(GAME_SIZE*0.5, GAME_SIZE - HALF_DISTANCE), radius=0.5*CELL),
            Player(name="Player 3", color=pygame.Color("blue"), position=(GAME_SIZE*0.5, GAME_SIZE - HALF_DISTANCE), radius=0.5*CELL)
        ]

    def play_game(self):
        current_player_index = 0
        while True:
            current_player = self.players[current_player_index]
            if current_player.is_ai:
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
                        success = current_player.update(event, self.nodes, self.walls, self.players)
                    self._render(current_player)                     
                   
            current_player_index = (current_player_index + 1) % len(self.players)

    def _render(self, current_player: Player):
        self.screen.fill(WHITE)
        self.walls.update()
        self.walls.draw(self.screen)
        self.nodes.draw(self.screen)
        self.player_group.draw(self.screen)
        self._render_metadata(current_player)
        pygame.display.flip()
    
    def _render_metadata(self, current_player: Player):
        self.screen.blit(
            self.font.render(f"Current player: {current_player.name}", False, (0, 0, 0)), 
            (GAME_SIZE, 0)
        )
        for i, player in enumerate(self.players):
            row = self.font_size * (i + 1) * 2
            self.screen.blit(
                self.font.render(f"{player.name}", False, (0, 0, 0)),
                (GAME_SIZE, row)
            )
            self.screen.blit(
                self.font.render(f"Total walls: {player.total_walls}", False, (0, 0, 0)), 
                (GAME_SIZE + 20, row + self.font_size)
            )

