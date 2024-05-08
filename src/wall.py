import pygame
from src.constants import DISTANCE, SMALL_CELL

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

    def update(self, events, current_player, walls):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        if not self.is_occupied:
            self.image = self.hover_image if hit else self.original_image

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                # wall can be placed
                # check curr wall and adjacent wall
                adjacent_wall = self.get_adjacent_wall(walls)
                if adjacent_wall:
                    adjacent_wall = adjacent_wall[0]
                    if not adjacent_wall.is_occupied:
                        self.place_wall()
                        self.place_adjacent_wall(adjacent_wall)
                        self.union_walls(adjacent_wall)

    def place_wall(self):
        self.is_occupied = True
        self.image = self.hover_image

    @staticmethod
    def place_adjacent_wall(adjacent_wall):
        adjacent_wall.place_wall()

    def get_adjacent_wall(self, walls):
        if self.horizontal:
            coordinate_to_search = tuple(map(sum, zip(self.position, (DISTANCE, 0))))
        else:
            coordinate_to_search = tuple(map(sum, zip(self.position, (0, DISTANCE))))
        wall = [wall for wall in walls if wall.position == coordinate_to_search]

        return wall

    def union_walls(self, adjacent_wall):
        if self.horizontal:
            self.image = self._create_image(TAN, adjacent_wall.w + self.w + SMALL_CELL, self.h)
        else:
            self.image = self._create_image(TAN, adjacent_wall.w, adjacent_wall.h + self.h + SMALL_CELL)

        self.rect = pygame.Rect.union(self.rect, adjacent_wall.rect)
        adjacent_wall.kill()



