from typing import NamedTuple

from pongpy.definitions import BALL_SIZE, ATK_SIZE, ATK_DELTA_LIMIT, DEF_SIZE, DEF_DELTA_LIMIT, BAR_WIDTH


class GameInfo(NamedTuple):
    """
    ゲームの設定値が入っているオブジェクト
    """
    width: int  # Pong フィールドの縦幅
    height: int  # Pong フィールドの横幅
    ball_size = BALL_SIZE  # ボールの大きさ
    atk_size = ATK_SIZE  # atk の縦幅
    atk_return_limit = ATK_DELTA_LIMIT  # 1 フレームでの atk の最大移動距離
    def_size = DEF_SIZE  # def の縦幅
    def_return_limit = DEF_DELTA_LIMIT  # 1 フレームでの def の最大移動距離
    bar_width = BAR_WIDTH  # atk, def の横幅
