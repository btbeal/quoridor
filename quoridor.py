import pygame
from src.assemble_board import assemble_board_component_groups
from src.constants import BOARD_SIZE
from src.player import assemble_player_group

nodes, walls = assemble_board_component_groups()
print(nodes)
players = assemble_player_group()
WHITE = (255, 255, 255)


class Quoridor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
        self.current_player = 1

    pygame.display.set_caption("Quoridor")

    def play_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for single_wall in walls:
                        if single_wall.rect.collidepoint(mouse_pos):
                            single_wall.update()

                self.screen.fill(WHITE)
                walls.draw(self.screen)
                nodes.draw(self.screen)
                players.draw(self.screen)
                pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    quoridor = Quoridor()
    quoridor.play_game()


