import numpy as np

import pygame
from pygame.sprite import Group

from src.node import Node
from src.player import Player
from src.board import Board
from src.constants import (
    SCREEN_SIZE_X,
    SCREEN_SIZE_Y,
    SPACES,
    GAME_SIZE,
    CELL,
    HALF_DISTANCE,
    WHITE,
    TERMINAL_NODE_Y,
    SEMI_BLACK,
    Direction,
)


DEFAULT_FONT_SIZE = 32


class Quoridor:
    def __init__(self, players=None, font_size=DEFAULT_FONT_SIZE):
        # Set up game infrastructure.
        pygame.init()
        pygame.display.set_caption("Quoridor")
        self.screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.font_size = font_size
        self.font = pygame.font.SysFont('Arial', font_size)

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
                success = False
                while not success:
                    state = self.board.get_state()
                    legal_move_dict = self._get_legal_moves(state=state, current_player_index=current_player_index)
                    random_move_type = np.random.choice(list(legal_move_dict.keys()))
                    potential_coordinates_for_move = legal_move_dict[random_move_type]
                    length_of_set = len(potential_coordinates_for_move)
                    index = np.random.choice(range(length_of_set))
                    coords = list(potential_coordinates_for_move)[index]
                    success = current_player.execute_legal_move(
                        board=self.board,
                        coordinate=coords,
                        move_type=random_move_type
                    )

                    self._render(current_player)

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
            current_player_index = (current_player_index + 1) % len(self.players)

    def _render(self, current_player: Player):
        self.screen.fill(WHITE)
        self.board.walls.update()
        self.board.walls.draw(self.screen)
        self.board.nodes.draw(self.screen)
        self.player_group.draw(self.screen)
        self._render_metadata(current_player)
        if self._is_winner(current_player):
            self._render_winner_screen(current_player=current_player)
        pygame.display.flip()

    def _render_metadata(self, current_player: Player):
        self.screen.blit(
            self.font.render(
                f"Current player: {current_player.name}", False, current_player.color
            ),
            (GAME_SIZE, 0),
        )
        for i, player in enumerate(self.players):
            row = self.font_size * (i + 1) * 2
            self.screen.blit(
                self.font.render(f"{player.name}", False, player.color), (GAME_SIZE, row)
            )
            self.screen.blit(
                self.font.render(
                    f"Total walls: {player.total_walls}", False, (0, 0, 0)
                ),
                (GAME_SIZE + 20, row + self.font_size),
            )

    @staticmethod
    def _is_winner(current_player):
        return TERMINAL_NODE_Y[current_player.index] == current_player.rect.center[1]

    def _render_winner_screen(self, current_player, font_name='Arial', font_size=48):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill(SEMI_BLACK)
        font = pygame.font.SysFont(font_name, font_size)
        winner_text = f"Player {current_player.index} Wins!"
        text_surface = font.render(winner_text, True, current_player.color)
        text_rect = text_surface.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = True

    def _get_legal_moves(self, state, current_player_index):
        eligible_wall_center_coords = self._get_eligible_wall_centers(state)
        eligible_node_center_coords = self._get_eligible_node_centers(state, current_player_index)
        move_dict = {
            'place_wall': eligible_wall_center_coords,
            'move_pawn': eligible_node_center_coords
        }

        return move_dict

    @staticmethod
    def _get_eligible_wall_centers(state):
        rows, cols = state.shape
        eligible_coords = set()

        for i in range(rows):
            j = 1
            while j <= cols - 3:
                if state[i, j] == 2 and state[i, j + 1] == 2 and state[i, j + 2] == 2:
                    eligible_coords.add((i, j + 1))  # Add the center coordinate
                j += 1

        for j in range(cols):
            i = 1
            while i <= rows - 3:
                if state[i, j] == 2 and state[i + 1, j] == 2 and state[i + 2, j] == 2:
                    eligible_coords.add((i + 1, j))  # Add the center coordinate
                i += 1

        return eligible_coords

    def _get_eligible_node_centers(self, state, current_player_index, max_dim=SPACES):
        for player in self.players:
            if player.index != current_player_index:
                x_opponent, y_opponent = np.argwhere(state == player.matrix_representation)[0]
            else:
                x, y = np.argwhere(state == player.matrix_representation)[0]

        current_coords = tuple((x, y))
        eligible_coords = set()
        occupied_walls_around_current_node_dict = self.board.get_walls_around_node(
            normalized_node_coordinates=current_coords,
            state=state
        )
        for direction in Direction:
            node_direction_to_add = Node.get_coordinates_in_direction(direction=direction, use_normalized=True)
            new_node_coords = Board.add_coordinates(current_coords, node_direction_to_add)
            x_bool = (0 <= new_node_coords[0] < max_dim)
            y_bool = (0 <= new_node_coords[1] < max_dim)
            coords_are_opponents = new_node_coords == (x_opponent, y_opponent)
            if not occupied_walls_around_current_node_dict.get(direction):
                if x_bool and y_bool and not coords_are_opponents:
                    eligible_coords.add(new_node_coords)
                elif coords_are_opponents:
                    occupied_walls_around_opponent_node_dict = self.board.get_walls_around_node(
                        normalized_node_coordinates=new_node_coords,
                        state=state
                    )

                    nodes_around_opponent_node_dict = self.board.get_nodes_around_node(
                        normalized_node_coordinates=new_node_coords,
                        state=state
                    )

                    if not occupied_walls_around_opponent_node_dict.get(direction) and nodes_around_opponent_node_dict.get(direction):
                        eligible_coords.add(nodes_around_opponent_node_dict[direction])
                    elif occupied_walls_around_opponent_node_dict.get(direction): # wall behind opponent node
                        if direction in [Direction.UP, Direction.DOWN]:
                            for direct in [Direction.LEFT, Direction.RIGHT]:
                                if not occupied_walls_around_opponent_node_dict.get(direct) and nodes_around_opponent_node_dict.get(direct):
                                    eligible_coords.add(nodes_around_opponent_node_dict[direct])
                        else:
                            for direct in [Direction.UP, Direction.DOWN]:
                                if not occupied_walls_around_opponent_node_dict.get(direct) and nodes_around_opponent_node_dict.get(direct):
                                    eligible_coords.add(nodes_around_opponent_node_dict[direct])

        return eligible_coords






