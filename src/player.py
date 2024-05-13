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
                    pressed_keys = pygame.key.get_pressed()
                    current_node = self._current_node(nodes)
                    if pressed_keys[pygame.K_a] and any(pressed_keys[key] for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]):
                        if event.key == pygame.K_UP:
                            success = self._move_adjacent(nodes, walls, current_node, 'up')
                        if event.key == pygame.K_DOWN:
                            success = self._move_adjacent(nodes, walls, current_node, 'down')
                        if event.key == pygame.K_RIGHT:
                            success = self._move_adjacent(nodes, walls, current_node, 'right')
                        if event.key == pygame.K_LEFT:
                            success = self._move_adjacent(nodes, walls, current_node, 'left')
                    elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
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

        if proximal_wall:
            if not proximal_wall.is_occupied:
                if proximal_node:
                    if not proximal_node.is_occupied:
                        self.rect.center = proximal_node.rect.center
                        proximal_node.is_occupied = True
                        current_node.is_occupied = False
                        return True
                    else:
                        next_proximal_wall = get_proximal_object(proximal_node.rect.center, direction, HALF_DISTANCE, walls)
                        if next_proximal_wall and not next_proximal_wall.is_occupied:
                            next_proximal_node = get_proximal_object(proximal_node.rect.center, direction, DISTANCE, nodes)
                            self.rect.center = next_proximal_node.rect.center
                            next_proximal_node.is_occupied = True
                            current_node.is_occupied = False
                            return True

        return False

    def _move_adjacent(self, nodes, walls, current_node, direction):
        # Check surrounding nodes
        # Find the node that is occupied
        # ensure the direction, from that node, is not occupied/blocked by any walls
        # move that direction
        print(isinstance(walls.sprites()[0], Wall))
        proximal_node = get_proximal_object(self.rect.center, direction, DISTANCE, nodes)
        proximal_wall = get_proximal_object(self.rect.center, direction, HALF_DISTANCE, walls)

        if proximal_node and proximal_node.is_occupied:
            if proximal_wall and not proximal_wall.is_occupied:
                wall_in_adjacent_direction = get_proximal_object(proximal_node.rect.center, direction, HALF_DISTANCE, walls)
                if wall_in_adjacent_direction and not wall_in_adjacent_direction.is_occupied:
                    next_proximal_node = get_proximal_object(proximal_node.rect.center, direction, DISTANCE, nodes)
                    self.rect.center = next_proximal_node.rect.center
                    next_proximal_node.is_occupied = True
                    current_node.is_occupied = False
                    return True

        return False


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

