import numpy as np
import pygame

from src.constants import Direction
from src.board import Board
from src.utils import get_proximal_object
from src.node import Node
from src.wall import Wall


class Player(pygame.sprite.Sprite):
    total_walls = 10

    def __init__(self, index, name, position, color, radius, is_ai=False):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.index = index
        self.matrix_representation = (index + 1) * 10
        self.name = name
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=position)
        self.position = position

        # ai attributes
        self.is_ai = is_ai
        self.epsilon = 0.0

    def update(
        self,
        event,
        board: Board,
        players,
    ) -> bool:
        """
        Returns whether the given event is a valid move and updates the state of the board
        if so.
        """
        if event.type == pygame.KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            current_node = self._current_node(board.nodes)
            key_list = [key for key in iter(Direction) if pressed_keys[key]]
            total_keys_pressed = sum(pressed_keys)

            if pressed_keys[pygame.K_a] and key_list and total_keys_pressed <= 2:
                adjacent_movement = key_list[0]
                return self._move_adjacent(board, current_node, adjacent_movement)

            if key_list:
                movement = key_list[0]
                return self._move(board.nodes, current_node, board.walls, movement)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            walls_to_place = [
                wall for wall in board.walls if wall.rect.collidepoint(pos)
            ]
            num_walls_to_place = len(walls_to_place)
            if not num_walls_to_place:
                return False

            success = Player._place_wall(walls_to_place[0], board, players)
            if success:
                self.total_walls -= 1
                return True

        return False

    def _move(self, nodes, current_node, walls, movement):
        node_direction = Node.get_coordinates_in_direction(movement)
        proximal_node = get_proximal_object(self.rect.center, node_direction, nodes)

        wall_direction = Wall.get_coordinates_in_direction(movement)
        proximal_wall = get_proximal_object(self.rect.center, wall_direction, walls)

        if not proximal_wall or proximal_wall.is_occupied or not proximal_node:
            return False

        if not proximal_node.is_occupied:
            self.rect.center = proximal_node.rect.center
            proximal_node.is_occupied = True
            current_node.is_occupied = False
            return True

        next_proximal_wall = get_proximal_object(
            proximal_node.rect.center, wall_direction, walls
        )
        if next_proximal_wall and not next_proximal_wall.is_occupied:
            next_proximal_node = get_proximal_object(
                proximal_node.rect.center, node_direction, nodes
            )
            self.rect.center = next_proximal_node.rect.center
            next_proximal_node.is_occupied = True
            current_node.is_occupied = False
            return True

        return False

    def _move_adjacent(self, board: Board, current_node, adjacent_movement):
        current_node_position = current_node.rect.center
        surrounding_node_dict = board.get_objects_around_node(
            current_node_position, group=board.nodes, exclude_direction=None
        )

        occupied_nodes = [
            (direction, node)
            for direction, node in surrounding_node_dict.items()
            if node and node.is_occupied
        ]
        if occupied_nodes:
            occupied_node_information = occupied_nodes[0]
            occupied_node_object = occupied_node_information[
                1
            ]  # in two player game, only ever expect one occupied node
            occupied_node_direction = occupied_node_information[0]
            wall_direction = Wall.get_coordinates_in_direction(adjacent_movement)
            node_direction = Node.get_coordinates_in_direction(adjacent_movement)

            requested_node = get_proximal_object(
                occupied_node_object.rect.center, node_direction, board.nodes
            )
            wall_after_requested_node_direction = tuple(
                t / 2 for t in occupied_node_direction
            )

            wall_after_requested_node = get_proximal_object(
                occupied_node_object.rect.center,
                wall_after_requested_node_direction,
                board.walls,
            )
            potential_wall_blocking_path = get_proximal_object(
                occupied_node_object.rect.center, wall_direction, board.walls
            )
            if (
                requested_node
                and wall_after_requested_node.is_occupied
                and potential_wall_blocking_path
                and not potential_wall_blocking_path.is_occupied
            ):
                self.rect.center = requested_node.rect.center
                requested_node.is_occupied = True
                current_node.is_occupied = False
                return True

        return False

    def _current_node(self, nodes):
        for node in nodes:
            if node.position == self.rect.center:
                return node

        return None

    @staticmethod
    def _place_wall(wall: Wall, board: Board, players):
        adjacent_wall = board.get_adjacent_wall(wall)
        if adjacent_wall and not adjacent_wall.is_occupied:
            proposed_new_wall = pygame.Rect.union(wall.rect, adjacent_wall.rect)
            if not board.is_rect_intersecting_existing_wall(proposed_new_wall):
                adjacent_wall.is_occupied = True
                wall.is_occupied = True

                for player in players:
                    viable_path_remains = board.check_viable_path(
                        player.index, player.rect.center
                    )

                    if not viable_path_remains:
                        adjacent_wall.is_occupied = False
                        wall.is_occupied = False
                        return False

                wall.image = wall.hover_image
                wall._union_walls(adjacent_wall, proposed_new_wall)
                adjacent_wall.kill()

                return True

        return False

    @staticmethod
    def choose_from_legal_moves(legal_move_dict):
        random_move_type = np.random.choice(list(legal_move_dict.keys()))
        potential_coordinates_for_move = legal_move_dict[random_move_type]
        length_of_set = len(potential_coordinates_for_move)
        np.random.choice(range(length_of_set))

    def execute_legal_move(self, board, coordinate, move_type):
        current_node = self._current_node(board.nodes)
        print(current_node)
        if move_type == 'move_pawn':
            new_node = [node for node in board.nodes if board.normalize_coordinates(node.rect.center) == coordinate]
            new_node = new_node[0]
            self.rect.center = board.denormalize_coordinates(coordinate)
            new_node.is_occupied = True
            current_node.is_occupied = False
            return True
        else:
            for wall in board.walls:
                if board.normalize_coordinates(wall.rect.center) == coordinate:
                    return self._place_wall(wall, board=board, players=board.players)
