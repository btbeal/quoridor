from typing import Tuple

import numpy as np
from pygame.sprite import Group
from pygame.rect import Rect

from src.node import Node
from src.wall import Wall
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
            direction_vector = Direction.get_offset(Direction.DOWN, DISTANCE)
        else:
            direction_vector = Direction.get_offset(Direction.RIGHT, DISTANCE)

        coordinate_to_search = self.add_coordinates(direction_vector, wall.rect.center)
        for wall in self.walls:
            if wall.position == coordinate_to_search:
                return wall

        return None

    def is_rect_intersecting_existing_wall(self, rect: Rect):
        existing_walls = [wall for wall in self.walls if wall.is_occupied]
        return rect.collideobjects(existing_walls)

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
                neighbors = self.get_nodes_around_node(current_vertex)
                walls_between_neighbors = self.get_walls_around_node(current_vertex)
                valid_neighbors = []
                for direction, wall in walls_between_neighbors.items():
                    if wall and not wall.is_occupied:
                        valid_neighbors.append(neighbors[direction])

                for neighboring_node in valid_neighbors:
                    if neighboring_node.position not in seen:
                        if neighboring_node.position[1] == terminal_y_coord:
                            return True
                        else:
                            stack.append(neighboring_node.position)

        return False

    def get_state(self):
        """
        Represents the board as 17 X 17 (SPACES X SPACES) matrix with the following notation:
            2 = all unoccupied walls
            1 = all occupied walls
            0 = all unoccupied nodes
            player number * 10 = player position (and thus the only occupied nodes)
        :return: matrix
        """
        game_state = np.full((SPACES, SPACES), 2)

        for wall in self.walls:
            normalized_coordinates = self.normalize_coordinates(wall.rect.center)
            if wall.is_occupied:
                x_coord = normalized_coordinates[0]
                y_coord = normalized_coordinates[1]
                if wall.is_vertical:
                    game_state[x_coord, y_coord + 1] = 1
                    game_state[x_coord, y_coord - 1] = 1
                    game_state[normalized_coordinates] = 1
                else:
                    game_state[x_coord + 1, y_coord] = 1
                    game_state[x_coord - 1, y_coord] = 1
                    game_state[normalized_coordinates] = 1
            else:
                game_state[normalized_coordinates] = 2

        for node in self.nodes:
            normalized_coordinates = self.normalize_coordinates(node.rect.center)
            if not node.is_occupied:
                game_state[normalized_coordinates] = 0

        for player in self.players:
            normalized_coordinates = self.normalize_coordinates(player.rect.center)
            game_state[normalized_coordinates] = player.matrix_representation

        return game_state

    @staticmethod
    def normalize_coordinates(coords, distance=HALF_DISTANCE):
        return tuple(int(coord / distance) - 1 for coord in coords)

    @staticmethod
    def add_coordinates(a, b):
        x = int(a[0] + b[0])
        y = int(a[1] + b[1])

        return tuple((x, y))

    def get_walls_around_node(self, node_coordinates, directions=Direction):
        walls_around_node = {}
        for direction in directions:
            wall_vector = Wall.get_coordinates_in_direction(direction=direction)
            wall_coords = self.add_coordinates(node_coordinates, wall_vector)
            wall = next(
                (wall for wall in self.walls if wall.rect.center == wall_coords),
                None
            )

            walls_around_node[direction] = wall

        return walls_around_node

    def get_nodes_around_node(self, node_coordinates, directions=Direction):
        nodes_around_node = {}
        for direction in directions:
            node_vector = Node.get_coordinates_in_direction(direction=direction)
            node_coords = self.add_coordinates(node_coordinates, node_vector)
            node = next(
                (node for node in self.nodes if node.rect.center == node_coords),
                None
            )

            nodes_around_node[direction] = node

        return nodes_around_node

    def get_direction_of_proximal_player(self, current_player):
        nodes_around_player = self.get_nodes_around_node(current_player.rect.center)
        for direction, node in nodes_around_player.items():
            if node and node.is_occupied:
                return direction

        return None





