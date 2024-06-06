import pygame
from src.player import Player
from src.constants import GAME_SIZE, SEMI_BLACK, WHITE


class RenderMixin:
    def _render(self, current_player: Player, render_win_screen=False):
        self.screen.fill(WHITE)
        self.board.walls.update()
        self.board.walls.draw(self.screen)
        self.board.nodes.draw(self.screen)
        self.player_group.draw(self.screen)
        self._render_metadata(current_player)
        if self._is_winner(current_player) and render_win_screen:
            self._render_winner_screen(current_player=current_player)
        pygame.display.flip()

    def _render_metadata(self, current_player: Player):
        self.screen.blit(
            self.font.render(
                f"Current player: {current_player.name}", False, current_player.color
            ),
            (GAME_SIZE, 0),
        )
        for i, player in enumerate(self.players):
            row = self.font_size * (i + 1) * 2
            self.screen.blit(
                self.font.render(f"{player.name}", False, player.color), (GAME_SIZE, row)
            )
            self.screen.blit(
                self.font.render(
                    f"Total walls: {player.total_walls}", False, (0, 0, 0)
                ),
                (GAME_SIZE + 20, row + self.font_size),
            )

    def _render_winner_screen(self, current_player, font_name='Arial', font_size=48):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill(SEMI_BLACK)
        font = pygame.font.SysFont(font_name, font_size)
        winner_text = f"Player {current_player.index} Wins!"
        text_surface = font.render(winner_text, True, current_player.color)
        text_rect = text_surface.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = True