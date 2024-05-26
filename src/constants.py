from enum import IntEnum
import numpy as np
import pygame

SQUARES = 9
SPACES = SQUARES * 2 - 1  # This accounts for wall spacing
CELL = 50
SMALL_CELL = 10
DISTANCE = CELL + SMALL_CELL
HALF_DISTANCE = 0.5 * DISTANCE
CELL_WIDTHS = [HALF_DISTANCE for _ in range(SPACES)]
x = np.cumsum(CELL_WIDTHS)
INFO_PANEL_X = 400
GAME_SIZE = CELL_WIDTHS[-1] + x[-1]
SCREEN_SIZE_X = CELL_WIDTHS[-1] + x[-1] + INFO_PANEL_X
SCREEN_SIZE_Y = GAME_SIZE
TERMINAL_NODE_Y = [(SQUARES * DISTANCE) - HALF_DISTANCE, HALF_DISTANCE]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
SEMI_BLACK = (0, 0, 0, 128)


class Direction(IntEnum):
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT

    @classmethod
    def get_offset(cls, direction, distance):
        direction_map = {
            cls.RIGHT: (distance, 0),
            cls.LEFT: (-distance, 0),
            cls.UP: (0, -distance),
            cls.DOWN: (0, distance)
        }
        return direction_map.get(direction)

    @classmethod
    def get_adjacent_directions(cls, direction):
        adjacent_direction_map = {
            cls.RIGHT: [cls.UP, cls.DOWN],
            cls.LEFT: [cls.UP, cls.DOWN],
            cls.UP: [cls.RIGHT, cls.LEFT],
            cls.DOWN: [cls.RIGHT, cls.LEFT]
        }
        return adjacent_direction_map.get(direction)

    @classmethod
    def get_opposite_direction(cls, direction):
        opposite_direction_map = {
            cls.RIGHT: cls.LEFT,
            cls.LEFT: cls.RIGHT,
            cls.UP: cls.DOWN,
            cls.DOWN: cls.UP
        }
        return opposite_direction_map.get(direction)
