import pygame


class Node(pygame.sprite.Sprite):
    def __init__(self, color=pygame.Color('gray86'), position=(0, 0), w=50):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = self._create_image(color, w=w, h=w)
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






