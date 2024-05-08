import pygame

GRAY = (224, 224, 224)


class Node(pygame.sprite.Sprite):
    def __init__(self, color=GRAY, position=(0, 0), w=50):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, w])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.position = position
        self.is_occupied = False






