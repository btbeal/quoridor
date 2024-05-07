from pygame.sprite import Group
from src.node import Node
from src.wall import Wall
from src.constants import *


def assemble_board_component_groups():
    nodes = Group()
    walls = Group()

    for i in range(SPACES):
        for j in range(SPACES):
            x_coord = x[i]
            y_coord = x[j]
            if i % 2 == 0 and j % 2 == 0:  # Node
                nodes.add(Node(position=(x_coord, y_coord)))
            elif i % 2 == 0:  # Horizontal wall
                walls.add(Wall(position=(x_coord, y_coord)))
            elif j % 2 == 0:  # Vertical wall
                walls.add(Wall(position=(x_coord, y_coord), horizontal=False))

    return nodes, walls
