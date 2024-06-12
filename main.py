import pygame

from src.quoridor import Quoridor
from src.player import Player, AIPlayer
from src.constants import GAME_SIZE, HALF_DISTANCE, CELL

players = [
    Player(
        index=0,
        name="Orange",
        color=pygame.Color("coral"),
        position=(GAME_SIZE * 0.5, HALF_DISTANCE),
        radius=0.5 * CELL
    ),
    Player(
        index=1,
        name="Blue",
        color=pygame.Color("blue"),
        position=(GAME_SIZE * 0.5, GAME_SIZE - HALF_DISTANCE),
        radius=0.5 * CELL
    ),
]


if __name__ == "__main__":
    quoridor = Quoridor(players=players)
    quoridor.run_game()
