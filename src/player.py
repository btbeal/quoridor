from collections import deque
import numpy as np
import pygame
import torch
import torch.nn as nn


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
        self.is_ai = is_ai

    def current_node(self, nodes):
        for node in nodes:
            if node.position == self.rect.center:
                return node

        return None

    def place_wall(self, board, coords):
        validated_wall = next(wall for wall in board.walls if wall.rect.center == coords)
        adjacent_wall = board.get_adjacent_wall(validated_wall)
        proposed_new_wall = pygame.Rect.union(validated_wall.rect, adjacent_wall.rect)
        validated_wall.is_occupied = True
        validated_wall.image = validated_wall.hover_image
        validated_wall.union_walls(adjacent_wall, proposed_new_wall)
        adjacent_wall.kill()
        self.total_walls -= 1

    def move_player(self, board, coords):
        nodes = board.nodes
        new_node = next(node for node in nodes if node.rect.center == coords)
        current_node = self.current_node(nodes)
        current_node.is_occupied = False
        new_node.is_occupied = True
        self.rect.center = new_node.rect.center


class AIPlayer(Player):
    def __init__(self, index, name, position, color, radius):
        super().__init__(index, name, position, color, radius, is_ai=True)


