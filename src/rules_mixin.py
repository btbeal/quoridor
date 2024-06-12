from src.directions import Direction
import pygame


class QuoridorRulesMixin:
    def _get_legal_moves(self, current_player):
        eligible_wall_coords = []
        if current_player.total_walls > 0:
            walls = self._get_legal_walls()
            eligible_wall_coords = []
            for wall in walls:
                eligible_wall_coords.append(wall.rect.center)

        eligible_lateral_moves = self._get_legal_lateral_moves(current_player)
        eligible_adjacent_moves = self._get_legal_adjacent_moves(current_player)

        pawn_move_dict = {**eligible_adjacent_moves, **eligible_lateral_moves}

        move_dict = {
            'place_wall': eligible_wall_coords,
            'move_pawn': pawn_move_dict
        }

        return move_dict

    def _get_legal_walls(self):
        """
        :return: a list of wall coordinates that are currently eligible to be placed
        """
        walls = self.board.walls
        legal_walls = []
        for wall in walls:
            if self._wall_is_legal(wall):
                legal_walls.append(wall)

        return legal_walls

    def _wall_is_legal(self, wall):
        board = self.board
        adjacent_wall = board.get_adjacent_wall(wall)
        if adjacent_wall and not adjacent_wall.is_occupied:
            proposed_new_wall = pygame.Rect.union(wall.rect, adjacent_wall.rect)
            if not board.is_rect_intersecting_existing_wall(proposed_new_wall):
                adjacent_wall.is_occupied = True
                wall.is_occupied = True

                for player in self.players:
                    viable_path_remains = board.check_viable_path(
                        player.index, player.rect.center
                    )

                    if not viable_path_remains:
                        adjacent_wall.is_occupied = False
                        wall.is_occupied = False
                        return False

                adjacent_wall.is_occupied = False
                wall.is_occupied = False
                return True

        return False

    def _get_legal_adjacent_moves(self, current_player):
        """
        :param current_player:
        :return: dictionary of structure {DirectionTuple: node} for  all eligible adjacent moves
        (if no eligible moves, returns {})
        """
        other_player_direction = self.board.get_direction_of_proximal_player(current_player)
        board = self.board
        eligible_adjacent_directions = {}
        if other_player_direction:
            other_player_node_dict = board.get_nodes_around_node(current_player.rect.center, [other_player_direction])
            other_player_node = other_player_node_dict[other_player_direction]
            adjacent_directions = Direction.get_adjacent_directions(other_player_direction)
            walls_around_player_node_dict = board.get_walls_around_node(current_player.rect.center, [other_player_direction])
            wall_between_players = walls_around_player_node_dict[other_player_direction]
            if wall_between_players and not wall_between_players.is_occupied:
                for direction in adjacent_directions:
                    is_legal_move, direction_tuple, node = self._is_legal_lateral_move(
                        direction, other_player_node.rect.center, current_player
                    )
                    if is_legal_move:
                        eligible_adjacent_directions[direction_tuple] = node

        return eligible_adjacent_directions

    def _get_legal_lateral_moves(self, current_player):
        """
        :param current_player:
        :return: dictionary of structure {DirectionTuple: node} for  all eligible moves (UP, DOWN, LEFT, RIGHT)
        (if no eligible moves, returns {})
        """
        legal_lateral_moves = {}
        starting_node = current_player.rect.center
        for direction in Direction:
            is_legal_move, direction_tuple, node = self._is_legal_lateral_move(direction, starting_node, current_player)
            if is_legal_move:
                legal_lateral_moves[direction_tuple] = node

        return legal_lateral_moves

    def _is_legal_lateral_move(self, direction, starting_node, current_player):
        board = self.board
        proximal_node_dict = board.get_nodes_around_node(starting_node, [direction])
        proximal_node = proximal_node_dict[direction]

        proximal_wall_dict = board.get_walls_around_node(starting_node, [direction])
        proximal_wall = proximal_wall_dict[direction]
        if not proximal_wall or proximal_wall.is_occupied or not proximal_node:
            return False, None, None

        if not proximal_node.is_occupied:
            return True, direction, proximal_node

        next_proximal_wall_dict = board.get_walls_around_node(proximal_node.rect.center, [direction])
        if next_proximal_wall_dict[direction] and not next_proximal_wall_dict[direction].is_occupied:
            next_proximal_node_dict = board.get_nodes_around_node(proximal_node.rect.center, [direction])
            next_proximal_node = next_proximal_node_dict[direction]
            return True, (direction, direction) if current_player.is_ai else direction, next_proximal_node

        return False, None, None