import pygame
from src.constants import DISTANCE, SMALL_CELL
from src.utils import get_new_position, dfs

WHITE = (255, 255, 255)
TAN = (210, 180, 140)
GRAY = (224, 224, 224)


class Wall(pygame.sprite.Sprite):
    def __init__(self, color=WHITE, position=(0, 0), w=50, h=10, horizontal=True):
        pygame.sprite.Sprite.__init__(self)
        self.horizontal = horizontal
        self.w = w if horizontal else h
        self.h = h if horizontal else w
        self.original_image = self._create_image(color, w=self.w, h=self.h)
        self.hover_image = self._create_image(color=TAN, w=self.w, h=self.h)
        self.image = self.original_image
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.rect.center = position
        self.position = position
        self.is_occupied = False

    @staticmethod
    def _create_image(color, w, h):
        img = pygame.Surface([w, h])
        img.fill(color)

        return img

    def update(self, events, walls):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        if not self.is_occupied:
            self.image = self.hover_image if hit else self.original_image

    def make_wall(self, walls, nodes, players):
        adjacent_wall = self._get_adjacent_wall(walls)
        if adjacent_wall and not adjacent_wall.is_occupied:
            proposed_new_wall = self._get_potential_union_rect(adjacent_wall)
            if not self._new_wall_intersects_existing_wall(new_rect=proposed_new_wall, walls=walls):
                curr_walls_with_proposed_new_wall = [proposed_new_wall] + [wall for wall in walls]

                for player in players:
                    viable_path_remains = dfs(
                        nodes=nodes,
                        walls=curr_walls_with_proposed_new_wall,
                        player=player
                    )

                    if not viable_path_remains:
                        return False

                self.is_occupied = True
                self.image = self.hover_image
                self._place_adjacent_wall(adjacent_wall)
                self._union_walls(adjacent_wall, proposed_new_wall)

                return True

        return False

    def _get_adjacent_wall(self, walls):
        if self.horizontal:
            coordinate_to_search = get_new_position(curr_position=self.position, direction='right', distance=DISTANCE)
        else:
            coordinate_to_search = get_new_position(curr_position=self.position, direction='down', distance=DISTANCE)

        for wall in walls:
            if wall.position == coordinate_to_search:
                return wall

        return None

    @staticmethod
    def _place_adjacent_wall(adjacent_wall):
        adjacent_wall.is_occupied = True
        adjacent_wall.image = adjacent_wall.hover_image

    def _get_potential_union_rect(self, adjacent_wall):
        return pygame.Rect.union(self.rect, adjacent_wall.rect)

    def _union_walls(self, adjacent_wall, new_rect):
        if self.horizontal:
            self.image = self._create_image(TAN, adjacent_wall.w + self.w + SMALL_CELL, self.h)
        else:
            self.image = self._create_image(TAN, adjacent_wall.w, adjacent_wall.h + self.h + SMALL_CELL)
        self.rect = new_rect

    @staticmethod
    def _new_wall_intersects_existing_wall(new_rect, walls):
        existing_walls = [wall for wall in walls if wall.is_occupied]

        return new_rect.collideobjects(existing_walls)
