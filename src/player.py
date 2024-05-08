import pygame
from pygame.sprite import Group
from src.constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, player_number, position, color, radius):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.player_number = player_number
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=position)

    def update(self, events, current_player):
        for event in events:
            if event.type == pygame.KEYDOWN and current_player == self.player_number:
                if event.key == pygame.K_UP:
                    self.rect.y -= DISTANCE
                if event.key == pygame.K_DOWN:
                    self.rect.y += DISTANCE
                if event.key == pygame.K_RIGHT:
                    self.rect.x += DISTANCE
                if event.key == pygame.K_LEFT:
                    self.rect.x -= DISTANCE


def assemble_player_group():
    player_group = Group()
    player_one = Player(player_number=1, color=pygame.Color("coral"), position=(BOARD_SIZE*0.5, HALF_DISTANCE), radius=0.5*CELL)
    player_two = Player(player_number=2, color=pygame.Color("blue"), position=(BOARD_SIZE*0.5, BOARD_SIZE - HALF_DISTANCE), radius=0.5*CELL)
    player_group.add([player_one, player_two])

    return player_group

