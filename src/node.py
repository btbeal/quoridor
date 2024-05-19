from typing import Tuple
import pygame

from src.constants import *


class Node(pygame.sprite.Sprite):
    def __init__(self, color=pygame.Color('gray86'), position=(0, 0), w=50):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = self._create_image(color, w=w, h=w)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.position = position
        self.is_occupied = False

    @staticmethod
    def _create_image(color, w, h):
        img = pygame.Surface([w, h])
        img.fill(color)
        return img
    
    @staticmethod
    def get_coordinates_in_direction(direction: int) -> Tuple[int, int]:
        if direction == pygame.K_LEFT:
            return (-DISTANCE, 0)
        if direction == pygame.K_RIGHT:
            return (DISTANCE, 0)
        if direction == pygame.K_UP:
            return (0, -DISTANCE)
        if direction == pygame.K_DOWN:
            return (0, DISTANCE)
        raise RuntimeError(f"Node direction {direction} not recognized")
