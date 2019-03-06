from typing import NamedTuple

from .pos import Pos


class TeamState(NamedTuple):
    atk_pos: Pos
    def_pos: Pos
    score: int  # 1セット内での得点数


class State(NamedTuple):
    is_right_side: bool  # 右側かどうか
    mine_team: TeamState  # 自チーム
    enemy_team: TeamState  # 相手チーム
    ball_pos: Pos  # ボール
    time: int  # 経過フレーム数
