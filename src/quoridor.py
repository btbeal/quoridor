import pygame
from pygame.sprite import Group

from src.player import Player
from src.board import Board
from src.constants import (
    SCREEN_SIZE_X,
    SCREEN_SIZE_Y,
    GAME_SIZE,
    CELL,
    HALF_DISTANCE,
    WHITE,
)


DEFAULT_FONT_SIZE = 32


class Quoridor:
    def __init__(self, players=None, font_size=DEFAULT_FONT_SIZE):
        # Set up game infrastructure.
        pygame.init()
        pygame.display.set_caption("Quoridor")
        self.screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, font_size)

        # Set up players and board.
        self.players = players if players else Quoridor.default_players()
        self.board = Board(self.players)
        self.player_group = Group()
        self.player_group.add(self.players)

    @staticmethod
    def default_players():
        return [
            Player(
                index=0,
                name="Orange",
                color=pygame.Color("coral"),
                position=(GAME_SIZE * 0.5, HALF_DISTANCE),
                radius=0.5 * CELL,
            ),
            Player(
                index=1,
                name="Blue",
                color=pygame.Color("blue"),
                position=(GAME_SIZE * 0.5, GAME_SIZE - HALF_DISTANCE),
                radius=0.5 * CELL,
            ),
        ]

    def play_game(self):
        current_player_index = 0
        while True:
            current_player = self.players[current_player_index]
            if current_player.is_ai:
                state = self.board.get_state()
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
                        success = current_player.update(event, self.board, self.players)
                    self._render(current_player)

    def _render(self, current_player: Player):
        self.screen.fill(WHITE)
        self.board.walls.update()
        self.board.walls.draw(self.screen)
        self.board.nodes.draw(self.screen)
        self.player_group.draw(self.screen)
        self._render_metadata(current_player)
        pygame.display.flip()

    def _render_metadata(self, current_player: Player):
        self.screen.blit(
            self.font.render(
                f"Current player: {current_player.name}", False, (0, 0, 0)
            ),
            (GAME_SIZE, 0),
        )
        for i, player in enumerate(self.players):
            row = self.font_size * (i + 1) * 2
            self.screen.blit(
                self.font.render(f"{player.name}", False, (0, 0, 0)), (GAME_SIZE, row)
            )
            self.screen.blit(
                self.font.render(
                    f"Total walls: {player.total_walls}", False, (0, 0, 0)
                ),
                (GAME_SIZE + 20, row + self.font_size),
            )
