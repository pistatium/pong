from typing import NamedTuple

from pongpy.definitions import BALL_SIZE, ATK_SIZE, ATK_DELTA_LIMIT, DEF_SIZE, DEF_DELTA_LIMIT, BAR_WIDTH


class GameInfo(NamedTuple):
    width: int
    height: int
    ball_size = BALL_SIZE
    atk_size = ATK_SIZE
    atk_return_limit = ATK_DELTA_LIMIT
    def_size = DEF_SIZE
    def_return_limit = DEF_DELTA_LIMIT
    bar_width = BAR_WIDTH
