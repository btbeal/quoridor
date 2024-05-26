import numpy as np
import time
import pygame
from pygame.sprite import Group

from src.board import Board
from src.constants import (
    SCREEN_SIZE_X,
    SCREEN_SIZE_Y,
    SPACES,
    GAME_SIZE,
    CELL,
    HALF_DISTANCE,
    TERMINAL_NODE_Y,
    Direction,
)
from src.node import Node
from src.player import Player
from src.render_mixin import RenderMixin


DEFAULT_FONT_SIZE = 32


class Quoridor(RenderMixin):
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
                    # get_legal_moves
                    # -- get_wall
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
                    pos = pygame.mouse.get_pos()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            wall_to_place = next(
                                (wall for wall in self.board.walls if wall.rect.collidepoint(pos))
                                , None
                            )
                            if not wall_to_place:
                                success = False

                            if self._wall_is_legal(wall_to_place) and current_player.total_walls > 0:
                                current_player.place_legal_wall(self.board, wall_to_place)
                                success = True
                        else:
                            success = current_player.update(event, self.board, self.players)
                    self._render(current_player)
                current_player_index = (current_player_index + 1) % len(self.players)

    @staticmethod
    def _is_winner(current_player):
        return TERMINAL_NODE_Y[current_player.index] == current_player.rect.center[1]

    def _get_legal_moves(self, state, current_player_index):
        current_player = self.players[current_player_index]
        eligible_wall_coords = []
        if current_player.total_walls > 0:
            walls = self._get_legal_walls()
            eligible_wall_coords = []
            for wall in walls:
                eligible_wall_coords.append(wall.rect.center)

        eligible_node_coords = self._get_eligible_node_coords(state, current_player_index)

        move_dict = {
            'place_wall': eligible_wall_coords,
            'move_pawn': eligible_node_coords
        }

        return move_dict

    def _get_legal_walls(self):
        walls = self.board.walls
        legal_walls = []
        for wall in walls:
            if self._wall_is_legal(wall):
                legal_walls.append(wall)

        return legal_walls

    def _wall_is_legal(self, wall):
        board = self.board
        adjacent_wall = self.board.get_adjacent_wall(wall)
        if adjacent_wall and not adjacent_wall.is_occupied:
            proposed_new_wall = pygame.Rect.union(wall.rect, adjacent_wall.rect)
            if not board.is_rect_intersecting_existing_wall(proposed_new_wall):
                adjacent_wall.is_occupied = True
                wall.is_occupied = True

                for player in self.players:
                    viable_path_remains = board.check_viable_path(
                        player.index, player.rect.center
                    )

                    if not viable_path_remains:
                        adjacent_wall.is_occupied = False
                        wall.is_occupied = False
                        return False

                adjacent_wall.is_occupied = False
                wall.is_occupied = False
                return True

        return False

    def _get_eligible_node_coords(self, state, current_player_index, max_dim=SPACES):
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
