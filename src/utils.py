import pygame
from src.constants import *
import src.wall

direction_dictionary = {
    pygame.K_LEFT: {'wall': (-HALF_DISTANCE, 0), 'node': (-DISTANCE, 0)},
    pygame.K_RIGHT: {'wall': (HALF_DISTANCE, 0), 'node': (DISTANCE, 0)},
    pygame.K_UP: {'wall': (0, -HALF_DISTANCE), 'node': (0, -DISTANCE)},
    pygame.K_DOWN: {'wall': (0, HALF_DISTANCE), 'node': (0, DISTANCE)}
}


def get_proximal_object(curr_position, direction, desired_object_group):
    new_coordinates = tuple(map(sum, zip(curr_position, direction)))
    for obj in desired_object_group:
        if obj.position == new_coordinates:
            return obj

    return None


def get_objects_around_node(
        curr_position,
        group,
        valid_directions,
        exclude_direction=None):
    proximal_objects = {}
    direction_list = [direction for direction in valid_directions if direction != exclude_direction and direction != pygame.K_a]
    for direction in direction_list:
        if isinstance(group.sprites()[0], src.wall.Wall):
            direction = direction_dictionary[direction]['wall']
            proximal_object = get_proximal_object(curr_position, direction, desired_object_group=group)
        else:
            direction = direction_dictionary[direction]['node']
            proximal_object = get_proximal_object(curr_position, direction, desired_object_group=group)

        proximal_objects[direction] = proximal_object

    return proximal_objects


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


def dfs(nodes, walls, player):
    seen = {}
    terminal_y_coord = TERMINAL_NODE_Y[player.player_number]
    stack = [player.rect.center]
    while len(stack) > 0:
        vertex = stack.pop()
        if vertex not in seen:
            current_vertex = vertex
            seen[current_vertex] = True
            stack.append(current_vertex)
            print(nodes)
            print(walls)
            neighbors = get_objects_around_node(current_vertex, group=nodes, valid_directions=direction_dictionary.keys())
            walls_between_neighbors = get_objects_around_node(current_vertex, group=walls, valid_directions=direction_dictionary.keys())
            valid_neighbors = []
            for direction, wall in walls_between_neighbors.items():
                if wall and not wall.is_occupied:
                    # multiply direction by 2 to get node direction from wall direction tuple
                    valid_direction = tuple(2*d for d in direction)
                    valid_neighbors.append(neighbors[valid_direction])

            for neighboring_node in valid_neighbors:
                if neighboring_node.position not in seen:
                    if neighboring_node.position[1] == terminal_y_coord:
                        return True
                    else:
                        stack.append(neighboring_node.position)

    return False


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


