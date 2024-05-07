import numpy as np

SQUARES       = 9
SPACES        = SQUARES * 2 - 1  # This accounts for wall spacing
CELL          = 50
SMALL_CELL    = 10
DISTANCE      = CELL + SMALL_CELL
HALF_DISTANCE = 0.5 * DISTANCE
CELL_WIDTHS   = [HALF_DISTANCE for _ in range(SPACES)]
x             = np.cumsum(CELL_WIDTHS)
BOARD_SIZE    = CELL_WIDTHS[-1] + x[-1]
