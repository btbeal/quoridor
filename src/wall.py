from typing import Tuple

import pygame

from src.constants import SMALL_CELL, HALF_DISTANCE


WHITE = (255, 255, 255)
TAN = (210, 180, 140)
GRAY = (224, 224, 224)


class Wall(pygame.sprite.Sprite):
    def __init__(self, color=WHITE, position=(0, 0), w=50, h=10, is_vertical=False):
        pygame.sprite.Sprite.__init__(self)
        self.is_vertical = is_vertical
        self.w = h if is_vertical else w
        self.h = w if is_vertical else h
        self.original_image = self._create_image(color, w=self.w, h=self.h)
        self.hover_image = self._create_image(color=TAN, w=self.w, h=self.h)
        self.image = self.original_image
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.rect.center = position
        self.position = position
        self.is_occupied = False

    @staticmethod
    def _create_image(color, w, h):
        img = pygame.Surface([w, h])
        img.fill(color)

        return img

    def update(self):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        if not self.is_occupied:
            self.image = self.hover_image if hit else self.original_image

    def _get_potential_union_rect(self, adjacent_wall):
        return pygame.Rect.union(self.rect, adjacent_wall.rect)

    def _union_walls(self, adjacent_wall, new_rect):
        if self.is_vertical:
            self.image = self._create_image(
                TAN, adjacent_wall.w, adjacent_wall.h + self.h + SMALL_CELL
            )
        else:
            self.image = self._create_image(
                TAN, adjacent_wall.w + self.w + SMALL_CELL, self.h
            )
        self.rect = new_rect

    @staticmethod
    def get_coordinates_in_direction(direction: int, use_normalized: bool = False) -> Tuple[int, int]:
        if use_normalized:
            distance = HALF_DISTANCE/HALF_DISTANCE
        else:
            distance = HALF_DISTANCE

        if direction == pygame.K_LEFT:
            return (-distance, 0)
        if direction == pygame.K_RIGHT:
            return (distance, 0)
        if direction == pygame.K_UP:
            return (0, -distance)
        if direction == pygame.K_DOWN:
            return (0, distance)
        raise RuntimeError(f"Wall direction {direction} not recognized")
