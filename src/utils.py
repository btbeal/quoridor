import pygame
from src.constants import *


def get_proximal_object(curr_position, direction, distance, desired_object_group):
    new_coordinates = get_new_position(curr_position, direction, distance)
    for obj in desired_object_group:
        if obj.position == new_coordinates:
            return obj

    return None


def get_new_position(curr_position, direction, distance):
    if direction == 'right':
        new_position = tuple(map(sum, zip(curr_position, (distance, 0))))
    elif direction == 'left':
        new_position = tuple(map(sum, zip(curr_position, (-distance, 0))))
    elif direction == 'up':
        new_position = tuple(map(sum, zip(curr_position, (0, -distance))))
    elif direction == 'down':
        new_position = tuple(map(sum, zip(curr_position, (0, distance))))

    return new_position


def display_player_walls(player_group, screen, cur_play, font_size=32):
    my_font = pygame.font.SysFont(None, font_size)
    coordinates = {
        'player_1': {'walls_remaining': (GAME_SIZE + 20, font_size*2), 'title': (GAME_SIZE, font_size)},
        'player_2': {'walls_remaining': (GAME_SIZE + 20, font_size*4), 'title': (GAME_SIZE, font_size*3)}
    }
    for i, player in enumerate(player_group):
        text_curr_player = my_font.render(f"Curr Player: {cur_play}", False, (0, 0, 0))
        text_surface_title = my_font.render(f"Player {player.player_number}", False, (0, 0, 0))
        text_surface_walls = my_font.render(f"Total Walls {player.total_walls}", False, (0, 0, 0))
        if i == 0:
            coords = coordinates['player_1']
        else:
            coords = coordinates['player_2']
        screen.blit(text_surface_title, coords['title'])
        screen.blit(text_surface_walls, coords['walls_remaining'])
        screen.blit(text_curr_player, (GAME_SIZE + 20, font_size * 6))


