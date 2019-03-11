from typing import NamedTuple


class Pos(NamedTuple):
    """
    フィールド内の相対座標
    左上が (0, 0) 。
    下に行くほど x が、右に行くほど y が増加する。
    """
    x: float
    y: float
