import pygame
import torch.optim

from src.quoridor import Quoridor
from src.player import Player, AIPlayer
from src.constants import GAME_SIZE, HALF_DISTANCE, CELL
from torch import nn
players = [
    AIPlayer(
        index=0,
        name="Orange",
        color=pygame.Color("coral"),
        position=(GAME_SIZE * 0.5, HALF_DISTANCE),
        radius=0.5 * CELL
    ),
    AIPlayer(
        index=1,
        name="Blue",
        color=pygame.Color("blue"),
        position=(GAME_SIZE * 0.5, GAME_SIZE - HALF_DISTANCE),
        radius=0.5 * CELL
    ),
]


if __name__ == "__main__":
    quoridor = Quoridor(players=players)
    state_size = len(quoridor.board.get_state())
    action_space_size = len(quoridor.action_space)
    for player in quoridor.players:
        if player.is_ai:
            player.append_model(state_size, action_space_size)

    quoridor.run_game()
