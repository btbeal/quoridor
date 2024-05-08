import pygame
from pygame.sprite import Group
from src.constants import *
from src.utils import get_new_position, get_proximal_object


class Player(pygame.sprite.Sprite):
    def __init__(self, player_number, position, color, radius):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.player_number = player_number
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=position)
        self.position = position

    def update(self, events, current_player, nodes, walls):
        for event in events:
            if event.type == pygame.KEYDOWN and current_player == self.player_number:
                current_node = self._current_node(nodes)
                if event.key == pygame.K_UP:
                    self._move(nodes, walls, current_node, 'up')
                if event.key == pygame.K_DOWN:
                    self._move(nodes, walls, current_node, 'down')
                if event.key == pygame.K_RIGHT:
                    self._move(nodes, walls, current_node, 'right')
                if event.key == pygame.K_LEFT:
                    self._move(nodes, walls, current_node, 'left')

    def _move(self, nodes, walls, current_node, direction):
        proximal_node = get_proximal_object(self.rect.center, direction, DISTANCE, nodes)
        proximal_wall = get_proximal_object(self.rect.center, direction, HALF_DISTANCE, walls)

        if proximal_wall and not proximal_wall.is_occupied:
            if proximal_node and not proximal_node.is_occupied:
                if direction == 'up':
                    self.rect.y -= DISTANCE
                elif direction == 'down':
                    self.rect.y += DISTANCE
                elif direction == 'left':
                    self.rect.x -= DISTANCE
                elif direction == 'right':
                    self.rect.x += DISTANCE

                proximal_node.is_occupied = True
                current_node.is_occupied = False
        else:
            print("ya can't do that")

    def _current_node(self, nodes):
        for node in nodes:
            if node.position == self.rect.center:
                return node

        return None

def assemble_player_group():
    player_group = Group()
    player_one = Player(player_number=1, color=pygame.Color("coral"), position=(BOARD_SIZE*0.5, HALF_DISTANCE), radius=0.5*CELL)
    player_two = Player(player_number=2, color=pygame.Color("blue"), position=(BOARD_SIZE*0.5, BOARD_SIZE - HALF_DISTANCE), radius=0.5*CELL)
    player_group.add([player_one, player_two])

    return player_group

