import pygame


class Node(pygame.sprite.Sprite):
    def __init__(self, color=pygame.Color('gray86'), position=(0, 0), w=50):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = self._create_image(color, w=w, h=w)
        self.hover_image = self._create_image(color=pygame.Color('aquamarine'), w=w, h=w)
        self.image = self.original_image
        self.rect = self.image.get_rect()
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

    def _is_hoverable(self, players, walls):
        # get the current player
        # assess all four potential surrounding walls
        #
        pass






