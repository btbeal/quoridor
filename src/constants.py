import numpy as np

SQUARES       = 9
SPACES        = SQUARES * 2 - 1  # This accounts for wall spacing
CELL          = 50
SMALL_CELL    = 10
DISTANCE      = CELL + SMALL_CELL
HALF_DISTANCE = 0.5 * DISTANCE
CELL_WIDTHS   = [HALF_DISTANCE for _ in range(SPACES)]
x             = np.cumsum(CELL_WIDTHS)
INFO_PANEL_X  = 400
GAME_SIZE     = CELL_WIDTHS[-1] + x[-1]
SCREEN_SIZE_X  = CELL_WIDTHS[-1] + x[-1] + INFO_PANEL_X
SCREEN_SIZE_Y  = GAME_SIZE

