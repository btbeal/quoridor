import pygame

WHITE = (255, 255, 255)
TAN = (210, 180, 140)
GRAY = (224, 224, 224)


class Wall(pygame.sprite.Sprite):
    def __init__(self, color=WHITE, position=(0, 0), w=50, h=10, horizontal=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h]) if horizontal else pygame.Surface([h, w])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.image.fill(TAN)
