from typing import NamedTuple

from .pos import Pos


class TeamState(NamedTuple):
    atk_pos: Pos
    def_pos: Pos
    score: int


class State(NamedTuple):
    reversed: bool
    mine_team: TeamState
    enemy_team: TeamState
    ball_pos: Pos
