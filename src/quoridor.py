import numpy as np
import pygame
from pygame.sprite import Group

from src.board import Board
from src.constants import (
    SCREEN_SIZE_X,
    SCREEN_SIZE_Y,
    GAME_SIZE,
    CELL,
    HALF_DISTANCE,
    TERMINAL_NODE_Y,
    Direction,
)

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

    def action_space(self):

    def play_game(self):
        current_player_index = 0
        while True:
            current_player = self.players[current_player_index]
            if current_player.is_ai:
                success = False
                while not success:
                    board = self.board
                    state = board.get_state()
                    legal_move_dict = self._get_legal_moves(current_player)
                    eligible_move_types = [key for key, value in legal_move_dict.items() if legal_move_dict[key]]
                    random_move_type = np.random.choice(eligible_move_types)
                    potential_coordinates_for_move = legal_move_dict[random_move_type]
                    length_of_set = len(potential_coordinates_for_move)
                    index = np.random.choice(range(length_of_set))
                    coords = list(potential_coordinates_for_move)[index]
                    if random_move_type == 'place_wall':
                        current_player.place_wall(board, coords)
                    else:
                        current_player.move_player(board, coords)

                    success=True

                current_player_index = (current_player_index + 1) % len(self.players)
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
                                current_player.place_wall(self.board, wall_to_place)
                                success = True
                        elif event.type == pygame.KEYDOWN:
                            pressed_keys = pygame.key.get_pressed()
                            key_list = [key for key in iter(Direction) if pressed_keys[key]]
                            total_keys_pressed = sum(pressed_keys)

                            if pressed_keys[pygame.K_a] and key_list and total_keys_pressed <= 2:
                                adjacent_movement = key_list[0]
                                legal_adjacent_moves = self._get_legal_adjacent_moves(current_player)
                                if adjacent_movement in legal_adjacent_moves:
                                    new_node = legal_adjacent_moves[adjacent_movement]
                                    current_player.move_player(new_node, self.board.nodes)
                                    success = True

                            elif key_list:
                                movement = key_list[0]
                                legal_lateral_moves = self._get_legal_lateral_moves(current_player)
                                if movement in legal_lateral_moves:
                                    new_node = legal_lateral_moves[movement]
                                    current_player.move_player(new_node, self.board.nodes)
                                    success = True

                    self._render(current_player)
                current_player_index = (current_player_index + 1) % len(self.players)

    @staticmethod
    def _is_winner(current_player):
        return TERMINAL_NODE_Y[current_player.index] == current_player.rect.center[1]

    def _get_legal_moves(self, current_player):
        eligible_wall_coords = []
        if current_player.total_walls > 0:
            walls = self._get_legal_walls()
            eligible_wall_coords = []
            for wall in walls:
                eligible_wall_coords.append(wall.rect.center)

        eligible_lateral_moves = self._get_legal_lateral_moves(current_player)
        eligible_lateral_move_coords = [node.rect.center for direction, node in eligible_lateral_moves.items() if node]
        eligible_adjacent_moves = self._get_legal_adjacent_moves(current_player)
        eligible_adjacent_move_coords = [node.rect.center for direction, node in eligible_adjacent_moves.items() if node]
        all_eligible_move_coords = eligible_lateral_move_coords + eligible_adjacent_move_coords

        move_dict = {
            'place_wall': eligible_wall_coords,
            'move_pawn': all_eligible_move_coords
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
        adjacent_wall = board.get_adjacent_wall(wall)
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

    def _get_legal_adjacent_moves(self, current_player):
        other_player_direction = self.board.get_direction_of_proximal_player(current_player)
        board = self.board
        eligible_adjacent_directions = {}
        if other_player_direction:
            other_player_node_dict = board.get_nodes_around_node(current_player.rect.center, [other_player_direction])
            other_player_node = other_player_node_dict[other_player_direction]
            adjacent_directions = Direction.get_adjacent_directions(other_player_direction)
            walls_around_player_node_dict = board.get_walls_around_node(current_player.rect.center, [other_player_direction])
            wall_between_players = walls_around_player_node_dict[other_player_direction]
            if wall_between_players and not wall_between_players.is_occupied:
                for direction in adjacent_directions:
                    is_legal_move, node = self._is_legal_lateral_move(direction, other_player_node.rect.center)
                    if is_legal_move:
                        eligible_adjacent_directions[direction] = node

        return eligible_adjacent_directions

    def _get_legal_lateral_moves(self, current_player):
        legal_lateral_moves = {}
        starting_node = current_player.rect.center
        for direction in Direction:
            is_legal_move, node = self._is_legal_lateral_move(direction, starting_node)
            if is_legal_move:
                legal_lateral_moves[direction] = node

        return legal_lateral_moves

    def _is_legal_lateral_move(self, direction, starting_node):
        board = self.board
        proximal_node_dict = board.get_nodes_around_node(starting_node, [direction])
        proximal_node = proximal_node_dict[direction]

        proximal_wall_dict = board.get_walls_around_node(starting_node, [direction])
        proximal_wall = proximal_wall_dict[direction]
        if not proximal_wall or proximal_wall.is_occupied or not proximal_node:
            return False, None

        if not proximal_node.is_occupied:
            return True, proximal_node

        next_proximal_wall_dict = board.get_walls_around_node(proximal_node.rect.center, [direction])
        if next_proximal_wall_dict[direction] and not next_proximal_wall_dict[direction].is_occupied:
            next_proximal_node_dict = board.get_nodes_around_node(proximal_node.rect.center, [direction])
            next_proximal_node = next_proximal_node_dict[direction]
            return True, next_proximal_node

        return False, None
