import pygame
from pygame.sprite import Group
from src.constants import *
from src.utils import get_proximal_object


class Player(pygame.sprite.Sprite):
    total_walls = 10

    def __init__(self, player_number, position, color, radius):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.player_number = player_number
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=position)
        self.position = position

    def update(self, events, nodes, walls, player_turn):
        success = False
        for event in events:
            if player_turn == self.player_number:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        current_node = self._current_node(nodes)
                        if event.key == pygame.K_UP:
                            success = self._move(nodes, walls, current_node, 'up')
                        if event.key == pygame.K_DOWN:
                            success = self._move(nodes, walls, current_node, 'down')
                        if event.key == pygame.K_RIGHT:
                            success = self._move(nodes, walls, current_node, 'right')
                        if event.key == pygame.K_LEFT:
                            success = self._move(nodes, walls, current_node, 'left')

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    success = self._place_wall(walls)
                    if success:
                        self.total_walls -= 1

        return success

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
                successful_move = True
        else:
            successful_move = False

        return successful_move

    @staticmethod
    def _place_wall(walls):
        pos = pygame.mouse.get_pos()
        successful_build = False
        for wall in walls:
            if wall.rect.collidepoint(pos):
                successful_build = wall.make_wall(walls)

        return successful_build

    def _current_node(self, nodes):
        for node in nodes:
            if node.position == self.rect.center:
                return node

        return None


def assemble_player_group():
    player_group = Group()
    player_one = Player(player_number=1, color=pygame.Color("coral"), position=(GAME_SIZE*0.5, HALF_DISTANCE), radius=0.5*CELL)
    player_two = Player(player_number=2, color=pygame.Color("blue"), position=(GAME_SIZE*0.5, GAME_SIZE - HALF_DISTANCE), radius=0.5*CELL)
    player_group.add([player_one, player_two])

    return player_group

