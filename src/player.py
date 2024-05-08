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
                if event.key == pygame.K_UP:
                    self._move_up(nodes, walls)
                    self.rect.y -= DISTANCE
                if event.key == pygame.K_DOWN:
                    self.rect.y += DISTANCE
                if event.key == pygame.K_RIGHT:
                    self.rect.x += DISTANCE
                if event.key == pygame.K_LEFT:
                    self.rect.x -= DISTANCE

    def _move_up(self, nodes, walls):
        node_coord_to_check = get_new_position(curr_position=self.rect.center, direction='down', distance=DISTANCE)
        immediate_wall_coord_to_check = get_new_position(curr_position=self.rect.center, direction='down', distance=DISTANCE)
        proximal_wall = get_proximal_object(
            curr_position=self.rect.center, direction='up', distance=HALF_DISTANCE, desired_object_group=walls
        )
        if proximal_wall:
            print(proximal_wall[0].is_occupied)
        # _validate_pawn_move() by...
        # check node below
            # if node occupied by pawn (node.is_occupied)
                # check for wall after pawn (wall.is_occupied)
                # if not wall_after_pawn
                # can jump (no need to assess if both nodes are occupied for two players)
        pass

    def _move_down(self):
        pass

    def _move_left(self):
        pass

    def _move_right(self):
        pass


def assemble_player_group():
    player_group = Group()
    player_one = Player(player_number=1, color=pygame.Color("coral"), position=(BOARD_SIZE*0.5, HALF_DISTANCE), radius=0.5*CELL)
    player_two = Player(player_number=2, color=pygame.Color("blue"), position=(BOARD_SIZE*0.5, BOARD_SIZE - HALF_DISTANCE), radius=0.5*CELL)
    player_group.add([player_one, player_two])

    return player_group

