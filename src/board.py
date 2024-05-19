from typing import Tuple, Union

import numpy as np
import pygame
from pygame.sprite import Group
from pygame.rect import Rect

from src.node import Node
from src.wall import Wall
from src.utils import get_proximal_object
from src.constants import DISTANCE, HALF_DISTANCE, SPACES, TERMINAL_NODE_Y, Direction, x


class Board:
    """
    Represents the game board. Responsible for maintaining state
    pertaining to the game board as well as calculating and providing
    information pertaining to said state.

    Specifically, maintains the following types of objects:
    1. Nodes
    2. Walls
    """

    def __init__(self, players):
        self.nodes, self.walls = self._construct_board()
        self.players = players

    def _construct_board(self) -> Tuple[list[Node], list[Wall]]:
        nodes = Group()
        walls = Group()
        for i in range(SPACES):
            for j in range(SPACES):
                x_coord = x[i]
                y_coord = x[j]
                if i % 2 == 0 and j % 2 == 0:  # Node
                    nodes.add(Node(position=(x_coord, y_coord)))
                elif i % 2 == 0:  # Horizontal wall
                    walls.add(Wall(position=(x_coord, y_coord)))
                elif j % 2 == 0:  # Vertical wall
                    walls.add(Wall(position=(x_coord, y_coord), is_vertical=True))
        return nodes, walls

    def get_adjacent_wall(self, wall: Wall):
        if wall.is_vertical:
            coordinate_to_search = self._get_new_position(
                curr_position=wall.position, direction=Direction.DOWN, distance=DISTANCE
            )
        else:
            coordinate_to_search = self._get_new_position(
                curr_position=wall.position,
                direction=Direction.RIGHT,
                distance=DISTANCE,
            )
        for wall in self.walls:
            if wall.position == coordinate_to_search:
                return wall

        return None

    def _get_new_position(self, curr_position, direction, distance):
        if direction == Direction.RIGHT:
            new_position = tuple(map(sum, zip(curr_position, (distance, 0))))
        elif direction == Direction.LEFT:
            new_position = tuple(map(sum, zip(curr_position, (-distance, 0))))
        elif direction == Direction.UP:
            new_position = tuple(map(sum, zip(curr_position, (0, -distance))))
        elif direction == Direction.DOWN:
            new_position = tuple(map(sum, zip(curr_position, (0, distance))))

        return new_position

    def is_rect_intersecting_existing_wall(self, rect: Rect):
        existing_walls = [wall for wall in self.walls if wall.is_occupied]
        return rect.collideobjects(existing_walls)

    def get_objects_around_node(
        self,
        curr_position,
        group: Union[list[Node], list[Wall]],
        exclude_direction=None,
    ):
        proximal_objects = {}
        direction_list = [
            direction
            for direction in iter(Direction)
            if direction != exclude_direction and direction != pygame.K_a
        ]
        for direction in direction_list:
            direction = group.sprites()[0].get_coordinates_in_direction(direction)
            proximal_object = get_proximal_object(
                curr_position, direction, desired_object_group=group
            )
            proximal_objects[direction] = proximal_object
        return proximal_objects

    def check_viable_path(self, player_index: int, player_center):
        seen = {}
        terminal_y_coord = TERMINAL_NODE_Y[player_index]
        stack = [player_center]
        while len(stack) > 0:
            vertex = stack.pop()
            if vertex not in seen:
                current_vertex = vertex
                seen[current_vertex] = True
                stack.append(current_vertex)
                neighbors = self.get_objects_around_node(
                    current_vertex, group=self.nodes
                )
                walls_between_neighbors = self.get_objects_around_node(
                    current_vertex, group=self.walls
                )
                valid_neighbors = []
                for direction, wall in walls_between_neighbors.items():
                    if wall and not wall.is_occupied:
                        # multiply direction by 2 to get node direction from wall direction tuple
                        valid_direction = tuple(2 * d for d in direction)
                        valid_neighbors.append(neighbors[valid_direction])

                for neighboring_node in valid_neighbors:
                    if neighboring_node.position not in seen:
                        if neighboring_node.position[1] == terminal_y_coord:
                            return True
                        else:
                            stack.append(neighboring_node.position)

        return False

    def get_state(self):
        game_state = np.zeros((SPACES, SPACES))

        for wall in self.walls:
            normalized_coordinates = self._normalize_coordinates(wall.rect.center)
            if wall.is_occupied:
                game_state[normalized_coordinates] = 1
            else:
                game_state[normalized_coordinates] = 2

        for player in self.players:
            normalized_coordinates = self._normalize_coordinates(player.rect.center)
            game_state[normalized_coordinates] = (player.index + 1) * 10

        return game_state

    @staticmethod
    def _normalize_coordinates(coords, distance=HALF_DISTANCE):
        return tuple(int(coord / distance) - 1 for coord in coords)
