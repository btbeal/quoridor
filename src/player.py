import pygame
from src.utils import get_proximal_object, get_objects_around_node, direction_dictionary


class Player(pygame.sprite.Sprite):
    total_walls = 10
    valid_directions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

    def __init__(self, name, position, color, radius, is_ai=False):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=position)
        self.position = position
        self.is_ai = is_ai

    def update(
            self,
            event,
            nodes,
            walls,
            players
    ) -> bool:
        """
        Returns whether the given event is a valid move and updates the state of the board
        if so.
        """
        if event.type == pygame.KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            current_node = self._current_node(nodes)
            key_list = [key for key in self.valid_directions if pressed_keys[key]]
            total_keys_pressed = sum(pressed_keys)

            if pressed_keys[pygame.K_a] and key_list and total_keys_pressed <= 2:
                adjacent_movement = key_list[0]
                return self._move_adjacent(nodes, current_node, walls, adjacent_movement)

            if key_list:
                movement = key_list[0]
                return self._move(nodes, current_node, walls, movement)

        if event.type == pygame.MOUSEBUTTONDOWN:
            success = Player._place_wall(walls, nodes, players)
            if success:
                self.total_walls -= 1
                return True

        return False

    def _move(self, nodes, current_node, walls, movement):
        node_direction = direction_dictionary[movement]['node']
        wall_direction = direction_dictionary[movement]['wall']
        proximal_node = get_proximal_object(self.rect.center, node_direction, nodes)
        proximal_wall = get_proximal_object(self.rect.center, wall_direction, walls)

        if not proximal_wall or proximal_wall.is_occupied or not proximal_node:
            return False
    
        if not proximal_node.is_occupied:
            self.rect.center = proximal_node.rect.center
            proximal_node.is_occupied = True
            current_node.is_occupied = False
            return True

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


