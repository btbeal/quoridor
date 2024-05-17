import pygame
from pygame.sprite import Group
from src.constants import *
from src.utils import get_proximal_object, get_objects_around_node, direction_dictionary


class Player(pygame.sprite.Sprite):
    total_walls = 10
    valid_directions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    def __init__(self, player_number, position, color, radius):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.player_number = player_number
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=position)
        self.position = position

    def update(
            self,
            events,
            nodes,
            walls,
            players,
            player_turn
    ):
        success = False
        for event in events:
            if player_turn == self.player_number:
                if event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()
                    current_node = self._current_node(nodes)
                    key_list = [key for key in self.valid_directions if pressed_keys[key]]
                    total_keys_pressed = sum(pressed_keys)

                    if pressed_keys[pygame.K_a] and key_list and total_keys_pressed <= 2:
                        adjacent_movement = key_list[0]
                        success = self._move_adjacent(nodes, current_node, walls, adjacent_movement)

                    elif key_list:
                        movement = key_list[0]
                        success = self._move(nodes, current_node, walls, movement)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    success = Player._place_wall(walls, nodes, players)
                    if success:
                        self.total_walls -= 1

        return success

    def _move(self, nodes, current_node, walls, movement):
        node_direction = direction_dictionary[movement]['node']
        wall_direction = direction_dictionary[movement]['wall']
        proximal_node = get_proximal_object(self.rect.center, node_direction, nodes)
        proximal_wall = get_proximal_object(self.rect.center, wall_direction, walls)

        if proximal_wall:
            if not proximal_wall.is_occupied:
                if proximal_node:
                    if not proximal_node.is_occupied:
                        self.rect.center = proximal_node.rect.center
                        proximal_node.is_occupied = True
                        current_node.is_occupied = False
                        return True
                    else:
                        next_proximal_wall = get_proximal_object(proximal_node.rect.center, wall_direction, walls)
                        if next_proximal_wall and not next_proximal_wall.is_occupied:
                            next_proximal_node = get_proximal_object(proximal_node.rect.center, node_direction, nodes)
                            self.rect.center = next_proximal_node.rect.center
                            next_proximal_node.is_occupied = True
                            current_node.is_occupied = False
                            return True

        return False

    def _move_adjacent(self, nodes, current_node, walls, adjacent_movement):
        current_node_position = current_node.rect.center
        surrounding_node_dict = get_objects_around_node(
            current_node_position,
            group=nodes,
            valid_directions=self.valid_directions,
            exclude_direction=None
        )

        occupied_nodes = [(direction, node) for direction, node in surrounding_node_dict.items() if node and node.is_occupied]
        if occupied_nodes:
            occupied_node_information = occupied_nodes[0]
            occupied_node_object = occupied_node_information[1] # in two player game, only ever expect one occupied node
            occupied_node_direction = occupied_node_information[0]
            wall_direction = direction_dictionary[adjacent_movement]['wall']
            node_direction = direction_dictionary[adjacent_movement]['node']

            requested_node = get_proximal_object(occupied_node_object.rect.center, node_direction, nodes)
            wall_after_requested_node_direction = tuple(t/2 for t in occupied_node_direction)

            wall_after_requested_node = get_proximal_object(occupied_node_object.rect.center, wall_after_requested_node_direction, walls)
            potential_wall_blocking_path = get_proximal_object(occupied_node_object.rect.center, wall_direction, walls)
            if requested_node and wall_after_requested_node.is_occupied:
                if potential_wall_blocking_path and not potential_wall_blocking_path.is_occupied:
                    self.rect.center = requested_node.rect.center
                    requested_node.is_occupied = True
                    current_node.is_occupied = False
                    return True

        return False

    @staticmethod
    def _place_wall(walls, nodes, players):
        pos = pygame.mouse.get_pos()
        successful_build = False
        for wall in walls:
            if wall.rect.collidepoint(pos):
                return wall.make_wall(walls, nodes, players)

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

