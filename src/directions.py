from enum import IntEnum
import pygame


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
